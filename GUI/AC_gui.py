#!/usr/bin/env python3.9
"""
AC_gui.py - AutoCCS GUI Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides graphical user interface functionality for the AutoCCS tool.
    It manages Docker container orchestration for automated CCS calculations with GUI support.
    The module handles various experiment types and supports optional feature annotation.
    
    Key Features:
    - Docker container management for AutoCCS execution via GUI
    - Support for single, SLIM, and stepped field experiments
    - Optional feature annotation capabilities
    - Timestamps for logging
    - Cross-platform file handling
"""

import sys
import docker
import os
import tarfile
import time
import platform
import shutil
import glob
import pathlib
from datetime import datetime


# Container runtime logging with timestamps
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

# R script commands for metadata extraction and annotation
command_0 = """Rscript /R_Metadata_I.R"""
command_tmp_fix_for_0 = """python3.8 /fix_metadata.py"""
command_annotate = """Rscript /R_Annotate_features_V.R"""
save_mem = os.path.join(os.getcwd(), "IV_data")


def run_container(exp, version, annotate, calibrant_file, framemeta_files, feature_files, 
                  target_list_file, raw_file_metadata, preP_files, autoccs_config):
    """
    Orchestrate AutoCCS Docker container execution for GUI.
    
    Parameters:
        exp (str): Experiment type - 'single', 'slim', or 'step'
        version (str): AutoCCS version - 'standard' or 'enhanced'
        annotate (bool): Whether to perform feature annotation
        calibrant_file (str): Path to calibrant file
        framemeta_files (str): Path to frame metadata files (for enhanced mode)
        feature_files (str): Path to feature CSV files
        target_list_file (str): Path to target list file (optional)
        raw_file_metadata (str): Path to raw file metadata (for SLIM)
        preP_files (str): Path to preprocessed files
        autoccs_config (str): Path to AutoCCS configuration file
        
    Returns:
        str: Path to the AutoCCS output directory
    """
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
    
    print("Save memory is: ", save_mem)
    
    #Make file system
    
    
    os.makedirs(os.path.join(save_mem, "PP"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "CF"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "TLF"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "FF"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "IV_Results"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "FMF"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "MD"), exist_ok=True)
    os.makedirs(os.path.join(save_mem, "CBF"), exist_ok=True)
    #Image name
    image = "anubhav0fnu/autoccs"   
    time.sleep(3)
    print("AutoCCS IV_data filesystem created")
    # Initialize Docker client and start container with volume mounts
    client = docker.from_env()
    print("AutoCCS Container Started")
    client.containers.run(image,name="AC_container",volumes={save_mem: {'bind': '/tmp', 'mode': 'rw'}}, detach=True, tty=True)
    AC_Container = client.containers.get('AC_container')

    print("AC container running")
    shutil.copy(autoccs_config, os.path.join(save_mem,"CF"))
    for file in list(pathlib.Path(feature_files).glob('*.csv')):
        shutil.copy(file, os.path.join(save_mem,"FF"))
    if exp == "single":
        for file in os.listdir(preP_files):
            d = os.path.join(preP_files, file)
            if os.path.isdir(d):
                if platform.system().upper() == "WINDOWS":
                    shutil.copytree("\\\\?\\" + d, os.path.join("\\\\?\\" + save_mem,"PP",file))
                else:
                    shutil.copytree(d, os.path.join(save_mem,"PP",file))
            else:
                if platform.system().upper() == "WINDOWS":
                    shutil.copy("\\\\?\\" + d, os.path.join("\\\\?\\" + save_mem,"PP",file))
                else:
                    shutil.copy(d, os.path.join(save_mem,"PP",file))
        
        shutil.copy(calibrant_file, os.path.join(save_mem,"CBF"))
    if exp == "slim":
        shutil.copy(raw_file_metadata, os.path.join(save_mem,"MD"))
        shutil.copy(calibrant_file, os.path.join(save_mem,"CBF"))
    if version == "enhanced":
        for file in list(pathlib.Path(framemeta_files).glob('*.txt')):
            shutil.copy(file, os.path.join(save_mem,"FMF"))
    if exp == "step":
        shutil.copy(target_list_file, os.path.join(save_mem,"TLF"))
    time.sleep(5)
    if annotate == True:
        shutil.copy(target_list_file, os.path.join(save_mem,"TLF"))

    #single field performs automated metadata extraction.
    #If this is ever not working, code can be modified to include this. See Notes in UI_V2.py.
    #slim requires user-generated metadata
    #stepped field determines metadata from filename.

    if exp == "single":
        AC_Container.exec_run(cmd=command_0)
        print("Metadata extracted")
        AC_Container.exec_run(cmd=command_tmp_fix_for_0)
        print("Metadata Fixed")
    time.sleep(3)
    print("Running AutoCCS")
    AC_Container.exec_run(cmd=command_list)
    print("AutoCCS Complete")
    time.sleep(3)
    if annotate == True:
        print("Annotation Script Running")
        AC_Container.exec_run(cmd=command_annotate)
        print("Annotations complete")
        time.sleep(3)
    #You can comment out .stop and .remove to use interactive mode with the AC_Container.
    AC_Container.stop()
    AC_Container.remove()
    return save_mem
   
