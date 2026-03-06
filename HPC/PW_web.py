#!/usr/bin/env python3.9

"""
PW_web.py - Proteowizard Web/MinIO Integration Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Web service integration for Proteowizard (msconvert) data conversion using
    MinIO S3-compatible object storage. Retrieves raw mass spectrometry files
    from MinIO storage and orchestrates Singularity container-based conversion
    with result management via MinIO. This module is in development and subject to API changes.
    
    This module bridges IMDASH web services with distributed Proteowizard
    processing infrastructure, enabling remote raw-to-mzML conversion with
    asynchronous result retrieval from cloud storage.
    
    Key Features:
    - MinIO S3-compatible object storage integration  
    - Remote raw data file retrieval for conversion
    - Singularity container execution with Wine emulation
    - Parallel data conversion processing
    - Automated result staging to object storage
    
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
    options = ["--bind", "/vagrant/dev_dockerized/drf/backend/PreProccessed_Data:/home/vagrant"]
    myinstance = Client.instance('../pwiz_sandbox', options=options)
    print("Instance name: ",myinstance,"   ",file)
    Client.execute(myinstance,["wine","msconvert", "/home/vagrant/" + file, "--outdir","/home/vagrant"])
    print("Instance complete: ",myinstance,"   ",file)

def run():
    # Initialize MinIO client for data retrieval
    minio_client = Minio("localhost:9000", access_key="minio", secret_key="minio123", secure=False)
    # Fetch preprocessed data archive from MinIO
    minio_client.fget_object("ion-mob-upload", "PreProcessedData_ZipFile", "PreProcessedData_ZipFile")
    # Extract tar archive to local processing directory
    my_tar = tarfile.open('/vagrant/dev_dockerized/drf/backend/PreProcessedData_ZipFile')
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
# Main
# 7) return data to minio

# NOTE: Previous Docker-based implementation replaced with Singularity container approach.
# Old Docker copy_a_file, copy_some_files, process, and run_container functions
# have been superseded by current Singularity-based run() function.
#Copy Functions: Copy from local Path to Path destination in a container.
#These require files to be in .tar format (so these are converted here, then transfered).

#Copy File functions (deprecated - replaced by Singularity implementation)
# Old Docker-based file transfer, process, and run_container functions removed.
# See git history for previous Docker container implementation.
