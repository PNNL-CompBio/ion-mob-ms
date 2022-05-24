#!/usr/bin/env python3.9

import sys
import docker
import os
import tarfile
import time

# config_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/autoCCS_config.xml"
# framemeta_files = '/Users/jaco059/OneDrive\ -\ PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/IV_ImsMetadata/*.txt'
# target_list_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/TargetList_NeutralMass.csv"
# feature_files = '/Users/jaco059/OneDrive\ -\ PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/IV_Features_csv/*.csv'


def copy_a_file(client, src,dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src) 
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()
    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)

def copy_some_files(client, src_list,dst):
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src,dst)



def run_container(config_file, framemeta_files, feature_files, target_list_file):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    
    cmd1 = "echo " + framemeta_files
    test1 = os.popen(cmd1).read()
    test1 = test1.strip()
    test1 = test1.split(" /")
    counter = 1
    for item in test1[1:]:
        test1[counter] =  "/" + item
        counter +=1

    cmd2 = "echo " + feature_files
    test2 = os.popen(cmd2).read()
    test2 = test2.strip()
    test2 = test2.split(" /")
    counter = 1
    for item in test2[1:]:
        test2[counter] =  "/" + item
        counter +=1

        

    command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_step_config.xml", "--framemeta_files",
    '/tmp/FMF/*.txt', "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--target_list_file", "/tmp/TLF/TargetList_NeutralMass.csv", "--mode", "multi"]

    image = "anubhav0fnu/autoccs"
    local_mem = os.getcwd() + "/tmp"
    print("the locaal mem : ", local_mem)
    
    #config_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/autoCCS_config.xml"


    os.makedirs("./tmp/CF", exist_ok=True)
    os.makedirs("./tmp/TLF", exist_ok=True)
    os.makedirs("./tmp/FF", exist_ok=True)
    os.makedirs("./tmp/FMF", exist_ok=True)
    os.makedirs("./tmp/IV_Results", exist_ok=True)
    print("Z\n")
    client = docker.from_env()
    print("Y\n")
    client.containers.run(image,name="AC_container",volumes={local_mem: {'bind': '/tmp', 'mode': 'rw'}}, detach=True, tty=True)
    print("A\n")
    copy_a_file(client, config_file, 'AC_container:/tmp/CF/config_file')
    print("B\n")
    copy_some_files(client, test1, 'AC_container:/tmp/FMF/framemeta_files')
    print("C\n")
    copy_some_files(client, test2, 'AC_container:/tmp/FF/feature_files')
    print("D\n")
    copy_a_file(client, target_list_file, 'AC_container:/tmp/TLF/target_list_file')
    print("E\n")
    AC_Container = client.containers.get('AC_container')
    time.sleep(5)
    print("F\n")
    AC_Container.exec_run(cmd=command_list)
    print("G\n")



