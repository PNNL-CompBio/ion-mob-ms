#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import sys
from minio import Minio
#from minio.error import S3Error
import os
import tarfile
import time
import platform
import pathlib
import threading
from multiprocessing import Pool
import io
import re
from spython.main import Client
import glob


#Set initial variables,
#Determine local mem


def process(file):
    options = ["--bind", "/vagrant/dev_dockerized/drf/backend/PreProccessed_Data:/home/vagrant"]
    myinstance = Client.instance('../pwiz_sandbox', options=options)
    print("Instance name: ",myinstance,"   ",file)
    Client.execute(myinstance,["wine","msconvert", "/home/vagrant/" + file, "--outdir","/home/vagrant"])
    print("Instance complete: ",myinstance,"   ",file)

def run():
    print("A")
    minio_client = Minio("localhost:9000", access_key="minio", secret_key="minio123", secure=False)
    print("B")
    minio_client.fget_object("ion-mob-upload", "PreProcessedData_ZipFile", "PreProcessedData_ZipFile")
    #main container
    print("C")
    my_tar = tarfile.open('/vagrant/dev_dockerized/drf/backend/PreProcessedData_ZipFile')
    #failing here
    my_tar.extractall('/vagrant/dev_dockerized/drf/backend/PreProccessed_Data')
    list_of_files = [os.path.basename(x) for x in glob.glob('/vagrant/dev_dockerized/drf/backend/PreProccessed_Data/*')]

    print("list_of_files: ", list_of_files)
    #individual containers (no cap?)
    process_num = len(list_of_files)
    if process_num > 10:
        process_num = 10
    pool = Pool(processes=process_num)
    pool.map(process, list_of_files)

    pool.close()
    pool.join()
    print("All Proteowizard instances complete")
    # mzML_files = [os.path.basename(x) for x in glob.glob('//vagrant/dev_dockerized/drf/backend/TEST_pipeline/PreProccessed_Data/*.mzML')]
    print("Cleaning residual files")
    print("Returning mzML files to minio")
    os.system("mkdir /vagrant/dev_dockerized/drf/backend/mzML_Files")
    os.system("mv /vagrant/dev_dockerized/drf/backend/PreProccessed_Data/*.mzML /vagrant/dev_dockerized/drf/backend/mzML_Files")

    with tarfile.open("mzML_Zipfile", "w:gz") as tar:
        for fn in os.listdir("/vagrant/dev_dockerized/drf/backend/mzML_Files"):
            p = os.path.join("/vagrant/dev_dockerized/drf/backend/mzML_Files", fn)
            tar.add(p, arcname=fn)

    minio_client.fput_object(
        "ion-mob-upload", "mzML_Zipfile", "/vagrant/dev_dockerized/drf/backend/mzML_Zipfile",
    )
    os.system("rm -r /vagrant/dev_dockerized/drf/backend/mzML_* /vagrant/dev_dockerized/drf/backend/PrePro*")
    ("\n_________________\nProteoWizard Complete.\n_________________\n")
    # OUTPUT= tarfile.open("mzML_Zipfile","w")
    # OUTPUT.add('//vagrant/dev_dockerized/drf/backend/TEST_pipeline/mzML_Files')
    # OUTPUT.close()



# steps: 
# Main
# 1) Open minio client. Copy PP data to location, untar it.
# 2) For each file in PP, run a container.
# Ind Container steps:
# 3) mount container
# 4) copy file to container. (or maybe not because it is mounted)
# 5) run proteowizard
# 6) close container
#  Main
# 7) return data to minio





#Copy Functions: Copy from local Path to Path destination in a container.
#These require files to be in .tar format (so these are converted here, then transfered).

#Copy File functions
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
#     os.remove((src + '.tar'))

# def copy_some_files(client, src_list,dst):
#     for src in src_list:
#         srcname = os.path.basename(src)
#         dst = dst + srcname
#         copy_a_file(client, src,dst)



# def process(filepath):
#     global client,image,local_mem,command_list
#     file_path = str(filepath.absolute())
#     cont_name = ("PW_container_" + os.path.basename(file_path))
#     client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, detach=True, tty=True)
#     print("Container started: ", cont_name)
#     PW_container = client.containers.get(cont_name)
#     copy_dst = cont_name + ":/III_mzML/"
#     copy_a_file(client, file_path,copy_dst)
#     print("Files copied to container: ", cont_name)
#     command_list.pop()
#     command_list.append(("/III_mzML/" + os.path.basename(file_path)))
#     print("Proteowizard msconvert started in container: ",cont_name)
#     PW_container.exec_run(cmd=command_list)
#     print("Proteowizard completed in container: ", cont_name)
    
#     PW_container.stop()
#     time.sleep(2)
#     PW_container.remove()

# def run_container(raw_file_folder,exptype):
#     global client,image,local_mem,command_list
#     cur_dir = os.path.dirname(__file__)
#     os.chdir(cur_dir)
#     local_mem = os.getcwd() + "/III_mzML"
#     print("ProteoWizard Working Directory: ", local_mem)
#     # print("directory is:", os.getcwd())
#     # print("local mem is: ", local_mem)
#     os.makedirs("./III_mzML", exist_ok = True)

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))

    #test for mac

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))

    # # if singlefield...
    # # if exptype == "Single":

    # #If Single field data is not Singlefield (determined by suffix), this will do something.
    # if exptype == "Single":
    #     print('Note: Running Single-Field Workflow, any files that do not contain ms1 data will be removed.')
    #     filtered_files =[]
    #     for item in file_list:
    #         ms_level = "no_suffix"
    #         raw_item = "{}".format(item)
    #         try:
    #             print("raw_item is:", raw_item)
    #             ms_level = re.search(r'\_([0-9]+)\.d', raw_item).group(1)
    #             print("ms level of ", raw_item, " is ", ms_level)
    #         except:
    #             pass
    #         if ms_level == "1" or ms_level == "no_suffix":
    #             filtered_files.append(item)
    #         else:
    #             print("File not included due to ms level indicated by naming suffix (..._2-#).d,: ", item)
    #     file_list = filtered_files

    # #This limits containers to 10 at a time. This is important for running locally.
    # #If this ever hits the cloud, "the limit does not exist!"
    # #This generates subprocesses - each subprocess runs a container which runs one file.
    # process_num = len(file_list)
    # if process_num > 10:
    #     process_num = 10

    # pool = Pool(processes=process_num)
    # pool.map(process, file_list)

    # pool.close()
    # pool.join()
    # return local_mem
