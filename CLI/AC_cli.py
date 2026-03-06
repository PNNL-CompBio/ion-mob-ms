#!/usr/bin/env python3.9
"""
AC_cli.py - AutoCCS Command Line Interface Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides command-line interface functionality for the AutoCCS tool.
    It manages Docker container orchestration for automated CCS (Collision Cross Section) 
    calculations. The module handles various experiment types (single field, SLIM, stepped field)
    and supports optional feature annotation.
    
    Key Features:
    - Docker container management for AutoCCS execution
    - File staging and metadata extraction
    - Support for single, SLIM, and stepped field experiments
    - Optional feature annotation capabilities
    - Cross-platform file handling (Windows, macOS, Linux)
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

# Runtime logging with timestamps for execution tracking
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
                  target_list_file, raw_file_metadata, preP_files, autoccs_config, autoccs_loc):
    """
    Orchestrate AutoCCS Docker container execution with appropriate parameters.
    
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
        autoccs_loc (str): Output directory for AutoCCS results
        
    Returns:
        str: Path to the AutoCCS output directory
    """
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    # Determine AutoCCS command list based on experiment type and version.
    # Command lists are maintained in verbose format for easy modification.
    # Note: Wildcards in file paths MUST use single quotes to prevent shell expansion.
    if version == "standard":
        if exp == "single":
            # Standard single field mode with automated metadata extraction
            command_list = ["python3.8", "/AutoCCS/autoCCS.py", "--config_file", 
                          ("/tmp/CF/" + os.path.basename(autoccs_config)), "--feature_files", '/tmp/FF/*.csv', 
                          "--sample_meta", "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", 
                          ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--output_dir", "/tmp/IV_Results", 
                          "--mode", "single", "--colname_for_filename", "RawFileName", 
                          "--tunemix_sample_type", "AgTune", "--colname_for_sample_type", "SampleType", 
                          "--single_mode", "batch"]

        elif exp == "slim":
            # Standard SLIM mode with user-provided metadata
            command_list = ["python3.8", "/AutoCCS/autoCCS.py", "--config_file", 
                          ("/tmp/CF/" + os.path.basename(autoccs_config)), "--feature_files", '/tmp/FF/*.csv', 
                          "--output_dir", "/tmp/IV_Results", "--sample_meta", 
                          ("/tmp/MD/" + os.path.basename(raw_file_metadata)), "--mode", "single", 
                          "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)),
                          "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "Calibrant", 
                          "--colname_for_sample_type", "SampleType", "--colname_for_ionization", "IonPolarity", 
                          "--single_mode", "batch", "--degree", "2", "--calib_method", "power"]
    
    if version == "enhanced": 
        if exp == "single":
            # Enhanced single field mode with frame metadata
            command_list = ["python3.8", "/AutoCCS/autoCCS.py", "--config_file", 
                          ("/tmp/CF/" + os.path.basename(autoccs_config)), "--framemeta_files", '/tmp/FMF/*.txt', 
                          "--sample_meta", "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", 
                          ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--feature_files", '/tmp/FF/*.csv', 
                          "--output_dir", "/tmp/IV_Results", "--mode", "single", 
                          "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "AgTune", 
                          "--colname_for_sample_type", "SampleType", "--single_mode", "batch"]
        elif exp == "step":
            # Enhanced stepped field mode with multi-level processing
            command_list = ["python3.8", "/AutoCCS/autoCCS.py", "--config_file", 
                          ("/tmp/CF/" + os.path.basename(autoccs_config)), "--framemeta_files", '/tmp/FMF/*.txt', 
                          "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", 
                          "--target_list_file", ("/tmp/TLF/" + os.path.basename(target_list_file)), "--mode", "multi"]
       
    # Log local and output directories
    print("Local memory is: ", save_mem)
    print("Output directory is: ", autoccs_loc)
    
    # Create directory structure for AutoCCS container
    os.makedirs(autoccs_loc + "/PP", exist_ok=True)
    os.makedirs(autoccs_loc + "/CF", exist_ok=True)
    os.makedirs(autoccs_loc + "/TLF", exist_ok=True)
    os.makedirs(autoccs_loc + "/FF", exist_ok=True)
    os.makedirs(autoccs_loc + "/IV_Results", exist_ok=True)
    os.makedirs(autoccs_loc + "/FMF", exist_ok=True)
    os.makedirs(autoccs_loc + "/MD", exist_ok=True)
    os.makedirs(autoccs_loc + "/CBF", exist_ok=True)
    
    # Docker image and startup
    image = "anubhav0fnu/autoccs"   
    time.sleep(3)
    print("AutoCCS directory structure created")
    
    # Start Docker container and mount local filesystem
    # Local filesystem is mounted to /tmp in container
    client = docker.from_env()
    print("Starting AutoCCS container")
    client.containers.run(image, name="AC_container", volumes={save_mem: {'bind': '/tmp', 'mode': 'rw'}}, 
                         detach=True, tty=True)
    AC_Container = client.containers.get('AC_container')
    print("AutoCCS container running")
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

    # Metadata extraction varies by experiment type:
    # - Single field: automated extraction from raw files
    # - SLIM: user-provided metadata required
    # - Stepped field: metadata derived from filenames

    if exp == "single":
        AC_Container.exec_run(cmd=command_0)
        print("Metadata extracted")
        AC_Container.exec_run(cmd=command_tmp_fix_for_0)
        print("Metadata Fixed")
    time.sleep(3)
    # Execute AutoCCS
    print("Running AutoCCS")
    AC_Container.exec_run(cmd=command_list)
    print("AutoCCS processing complete")
    time.sleep(3)
    
    # Optional feature annotation
    if annotate == True:
        print("Running feature annotation")
        AC_Container.exec_run(cmd=command_annotate)
        print("Annotation processing complete")
        time.sleep(3)
    
    # Clean up container
    AC_Container.stop()
    AC_Container.remove()
    return save_mem
   
