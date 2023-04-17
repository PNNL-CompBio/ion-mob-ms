#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import sys
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
from pathlib import Path
import shutil
import glob
import tqdm
from datetime import datetime

#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

#This step defines the run method of autoCCS.

command_0 = """Rscript /Work/R_Metadata_I.R"""
command_tmp_fix_for_0 = """python3.8 /Work/fix_metadata.py"""
command_annotate = """Rscript /Work/R_Annotate_features_V.R"""
local_mem = os.path.join(os.getcwd(), "IV_data")


def run_container(exp,version,annotate,calibrant_file,framemeta_files, feature_files, target_list_file,raw_file_metadata,preP_files,autoccs_config):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

#Determine which command line options will be used.
#This was kept in this longer format because it is easier to modify. 
#Note: If modifying these... any that use a wildcard, MUST use single quotes
#such as ('/tmp/FF/*.csv'). If you use double quotes, this will fail. Why? who knows...
    if version == "standard":
        if exp == "single":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", ("/tmp/CF/" + os.path.basename(autoccs_config)), "--feature_files", '/tmp/FF/*.csv', 
            "--sample_meta", "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--output_dir", "/tmp/IV_Results", "--mode", "single",
            "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "AgTune", "--colname_for_sample_type", "SampleType", "--single_mode", "batch"]

        elif exp == "slim":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", ("/tmp/CF/" + os.path.basename(autoccs_config)), "--feature_files", '/tmp/FF/*.csv', 
            "--output_dir", "/tmp/IV_Results", "--sample_meta", ("/tmp/MD/" + os.path.basename(raw_file_metadata)),"--mode", "single", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)),
            "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "Calibrant", "--colname_for_sample_type", "SampleType", "--colname_for_ionization", "IonPolarity", "--single_mode", "batch", "--degree", "2", "--calib_method", "power"]
    
    if version == "enhanced": 
        if exp == "single":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", ("/tmp/CF/" + os.path.basename(autoccs_config)), "--framemeta_files", '/tmp/FMF/*.txt', "--sample_meta", 
            "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--mode", 
            "single", "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "AgTune", "--colname_for_sample_type", "SampleType", "--single_mode", "batch"]
        elif exp == "step":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", ("/tmp/CF/" + os.path.basename(autoccs_config)), "--framemeta_files", '/tmp/FMF/*.txt', "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--target_list_file", ("/tmp/TLF/" + os.path.basename(target_list_file)), "--mode", "multi"]
       
    #This prints where the local files are being saved to. (With pyinstaller, this is a temporary folder)
    print("Local memory is: ", local_mem)
    #Image name
    # image = "anubhav0fnu/autoccs"    
    #Make file system
    os.makedirs("./IV_data/PP", exist_ok=True)
    os.makedirs("./IV_data/CF", exist_ok=True)
    os.makedirs("./IV_data/TLF", exist_ok=True)
    os.makedirs("./IV_data/FF", exist_ok=True)
    os.makedirs("./IV_data/IV_Results", exist_ok=True)
    os.makedirs("./IV_data/FMF", exist_ok=True)
    os.makedirs("./IV_data/MD", exist_ok=True)
    os.makedirs("./IV_data/CBF", exist_ok=True)
    time.sleep(3)
    print("AutoCCS IV_data filesystem created")
    #start container
    #mount local mem (path/IV_data) to /tmp in the container
    #in the container, all the subdirectories above are in /tmp path
    #Container is interactive. You can open a terminal (recc: then use bash) and see data & manually run autoCCS.
    # client = docker.from_env()
    # print("AutoCCS Container Started")
    
    options = ["--writable-tmpfs","--bind", local_mem +":/tmp"]
    myinstance = Client.instance('./autoccs.sif', options=options)
    AC_container = myinstance.name
    
    
    # client.containers.run(image,name="AC_container",volumes={local_mem: {'bind': '/tmp', 'mode': 'rw'}}, detach=True, tty=True)
    # AC_Container = client.containers.get('AC_container')

    print("AC container running")
    shutil.copy(autoccs_config, os.path.join(local_mem,"CF"))
    for file in glob.glob(feature_files):
        shutil.copy(file, os.path.join(local_mem,"FF"))
    if exp == "single":
        for file in os.listdir(preP_files):
            d = os.path.join(preP_files, file)
            print(d)
            if os.path.isdir(d):
                if platform.system().upper() == "WINDOWS":
                    shutil.copytree("\\\\?\\" + d, os.path.join("\\\\?\\" + local_mem,"PP",file))
                else:
                    shutil.copytree(d, os.path.join(local_mem,"PP",file))
            else:
                if platform.system().upper() == "WINDOWS":
                    shutil.copy("\\\\?\\" + d, os.path.join("\\\\?\\" + local_mem,"PP",file))
                else:
                    shutil.copy(d, os.path.join(local_mem,"PP",file))
        
        shutil.copy(calibrant_file, os.path.join(local_mem,"CBF"))
    if exp == "slim":
        shutil.copy(raw_file_metadata, os.path.join(local_mem,"MD"))
        shutil.copy(calibrant_file, os.path.join(local_mem,"CBF"))
    if version == "enhanced":
        for file in glob.glob(framemeta_files):
            shutil.copy(file, os.path.join(local_mem,"FMF"))
    if exp == "step":
        shutil.copy(target_list_file, os.path.join(local_mem,"TLF"))
    time.sleep(5)
    if annotate == True:
        shutil.copy(target_list_file, os.path.join(local_mem,"TLF"))

    #single field performs automated metadata extraction.
    #If this is ever not working, code can be modified to include this. See Notes in UI_V2.py.
    #slim requires user-generated metadata
    #stepped field determines metadata from filename.

    if exp == "single":
        Client.execute(myinstance,command_0, options=['--writable-tmpfs'],quiet=False)
        print("Metadata extracted")
        # AC_Container.exec_run(cmd=command_tmp_fix_for_0)
        Client.execute(myinstance,command_tmp_fix_for_0, options=['--writable-tmpfs'],quiet=False)
        
        print("Metadata Fixed")
    time.sleep(3)
    print("Running AutoCCS")
    # AC_Container.exec_run(cmd=command_list)
    Client.execute(myinstance,command_list, options=['--writable-tmpfs'],quiet=False)
    print("AutoCCS Complete")
    time.sleep(3)
    if annotate == True:
        print("Annotation Script Running")
        # AC_Container.exec_run(cmd=command_annotate)
        Client.execute(myinstance,command_annotate, options=['--writable-tmpfs'],quiet=False)
        print("Annotations complete")
        time.sleep(3)
    #You can comment out .stop and .remove to use interactive mode with the AC_Container.
    # myinstance.stop()
    # AC_Container.remove()
    return local_mem
   
