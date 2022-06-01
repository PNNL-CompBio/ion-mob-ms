#!/usr/bin/env python3.9

import sys
import docker
import os
import tarfile
import time



# batch_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/UserInterface/MZmine_FeatureFinder-batch.xml"

# def copy_a_file(client, src,dst):
#     name, dst = dst.split(':')
#     container = client.containers.get(name)
#     os.chdir(os.path.dirname(src))
#     srcname = os.path.basename(src) 
#     tar = tarfile.open(src + '.tar', mode='w')
#     try:
#         tar.add(srcname)
#     finally:
#         tar.close()
#     data = open(src + '.tar', 'rb').read()
#     container.put_archive(os.path.dirname(dst), data)

# def copy_some_files(client, src_list,dst):
#     for src in src_list:
#         srcname = os.path.basename(src)
#         dst = dst + srcname
#         copy_a_file(client, src,dst)

def run_container():
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    

    # command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_step_config.xml", "--framemeta_files",
    # '/tmp/FMF/*.txt', "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--target_list_file", "/tmp/TLF/TargetList_NeutralMass.csv", "--mode", "multi"]


    command_one = ["mv", "/tmp_mzmine/III_mzML", "/tmp"]
    command_two = ["mv", "/tmp_mzmine/MZmine_FeatureFinder-batch.xml", "/tmp"]
    image = "jjacobson95/mzmine2:latest"
    local_mem = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/UserInterface/tmp"

    print("Z\n")
    client = docker.from_env()
    print("Y\n")
    client.containers.run(image,name="MZ_Container",volumes={local_mem: {'bind': '/tmp', 'mode': 'rw'}}, detach=True, tty=True)
    MZ_Container = client.containers.get('MZ_Container')
    MZ_Container.exec_run(cmd=command_one)
    MZ_Container.exec_run(cmd=command_two)

    print("A\n")
    # copy_a_file(client, batch_file, 'MZ_Container:/tmp/xml_file')
    print("B\n")

run_container()

