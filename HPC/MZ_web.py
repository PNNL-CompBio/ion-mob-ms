#!/usr/bin/env python3.9

"""
MZ_web.py - MZmine Web/MinIO Integration Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Web service integration for MZmine feature detection using MinIO object
    storage backend. Retrieves mzML input files from MinIO S3-compatible storage
    and orchestrates Singularity container-based MZmine execution with results
    management via MinIO. This module is in development and subject to API changes.
    
    This module bridges IMDASH web services with high-performance MZmine
    processing infrastructure, enabling remote feature detection jobs with
    asynchronous result retrieval from cloud storage.
    
    Key Features:
    - MinIO S3-compatible object storage integration
    - Remote file retrieval for processing
    - Singularity container execution
    - XML batch configuration modification
    - Parallel feature detection processing
    
    Development Status: In active development - API and functionality subject to change
"""

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


def process(file):
    options = ["--bind", "/vagrant/dev_dockerized/drf/backend/mzMLData:/home/vagrant"]
    myinstance = Client.instance('../mzmine.sif', options=options)
    print("Instance name: ", myinstance, "   ", file)
    # Create temporary directory for processing
    Client.execute(myinstance, ["mkdir", "/home/vagrant/tmp"])
    # Copy batch configuration file to container
    Client.execute(myinstance, ["cp", "/Work/MZmine_FeatureFinder-batch.xml", "/home/vagrant/MZmine_FeatureFinder-batch.xml"])
    # Modify batch configuration with file-specific parameters
    tmp = "7s/.*/" + """        <parameter name="Raw data file names"><file>\/home\/vagrant\/""" + file + """<\/file><\/parameter>""" + "/"
    Client.execute(myinstance, ["sed", "-i", tmp, "/home/vagrant/MZmine_FeatureFinder-batch.xml"])
    # Execute MZmine feature detection
    Client.execute(myinstance, ["bash", "/MZmine-2.41.2/startMZmine_Linux.sh", "/home/vagrant/MZmine_FeatureFinder-batch.xml"])
    print("Instance complete: ", myinstance, "   ", file)

def run():
    minio_client = Minio("localhost:9000", access_key="minio", secret_key="minio123", secure=False)
    minio_client.fget_object("ion-mob-upload", "mzMLData_ZipFile", "mzMLData_ZipFile")
    #main container
    my_tar = tarfile.open('/vagrant/dev_dockerized/drf/backend/mzMLData_ZipFile')
    my_tar.extractall('/vagrant/dev_dockerized/drf/backend/mzMLData')
    list_of_files = [os.path.basename(x) for x in glob.glob('/vagrant/dev_dockerized/drf/backend/mzMLData/*.mzML')]

    print("list_of_files: ", list_of_files)
    #individual containers (no cap?)
    process_num = len(list_of_files)
    if process_num > 1:
        process_num = 1
    pool = Pool(processes=process_num)
    pool.map(process, list_of_files)

    pool.close()
    pool.join()
    print("All MZmine instances complete")
    print("Cleaning residual files")
    print("Returning mzML files to minio")
    os.system("mkdir /vagrant/dev_dockerized/drf/backend/IV_Features_csv")
    # os.system("ls /vagrant/dev_dockerized/drf/backend/")
    os.system("ls /vagrant/dev_dockerized/drf/backend/mzMLData")
    os.system("ls /vagrant/dev_dockerized/drf/backend/IV_Features_csv")

    os.system("mv /vagrant/dev_dockerized/drf/backend/mzMLData/*.csv /vagrant/dev_dockerized/drf/backend/IV_Features_csv")

    with tarfile.open("Feature_Zipfile", "w:gz") as tar:
        for fn in os.listdir("/vagrant/dev_dockerized/drf/backend/IV_Features_csv"):
            p = os.path.join("/vagrant/dev_dockerized/drf/backend/IV_Features_csv", fn)
            tar.add(p, arcname=fn)

    minio_client.fput_object(
        "ion-mob-upload", "Feature_Zipfile", "/vagrant/dev_dockerized/drf/backend/Feature_Zipfile",
    )
    os.system("rm -r /vagrant/dev_dockerized/drf/backend/mzMLData* /vagrant/dev_dockerized/drf/backend/IV_Features_csv* /vagrant/dev_dockerized/drf/backend/Feature_Zipfile")
    print("\n_________________\nMZmine Complete.\n_________________\n")



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

    # NOTE: Old run_container function implementation replaced by current MinIO-based approach
    # See git history for previous file list filtering and parallel processing logic
