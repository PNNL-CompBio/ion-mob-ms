#!/usr/bin/env python3.9
"""
PP_cli.py - PNNL PreProcessor Command Line Interface Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides command-line interface functionality for the PNNL PreProcessor tool.
    It orchestrates Docker container execution for smoothing and filtering raw ion mobility data.
    
    Note: This implementation is incomplete due to DLL compatibility issues with the Windows-based
    PNNL PreProcessor executable. The underlying tool management code is retained for future
    improvements or alternative implementations.
    
    Key Features:
    - Docker container orchestration for preprocessing
    - Cross-platform file handling (macOS, Windows)
    - Configurable drift and LC kernel parameters
    - File staging and data transfer
    
Limitations:
    - PNNL PreProcessor DLL issues prevent proper execution
    - Alternative preprocessing tools (e.g., embedded algorithms) are recommended
"""

import sys
import docker
import os
import tarfile
import time
import platform
import pathlib
import threading
from multiprocessing import Pool
import io

client = docker.from_env()
image = "jjacobson95/pnnl_preprocessor4"    
local_mem = os.getcwd() + "/II_Preprocessed"
command_0 = """Rscript /tmp/R_Metadata_I.R"""
# PNNL-PreProcessor command with parameters
command_list_1 = ["C:\\PNNL-Preprocessor_4.0_2022.02.17\\PNNL-Preprocessor\\PNNL-PreProcessor.exe", 
                  "-smooth", "-driftKernel", "1", "-lcKernel", "0", "-minIntensity", "20", "-split", "-r", "-d", 
                  '"..\\..\\tmp\\II_Preprocessed\\I_Raw"']


def copy_a_file(client, src, dst):
    """
    Copy a file to a Docker container using tar archive. Handles platform differences.
    
    Parameters:
        client: Docker client instance
        src (str): Source file path on host
        dst (str): Destination in container format 'container_name:/path' (macOS) or 'container_nameC:\\path' (Windows)
    """
    if platform.system().upper() == "DARWIN":
        name, dst = dst.split(':')
    if platform.system().upper() == "WINDOWS":
        name = dst[:-6]
        dst = dst[-6:]
    
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
    os.remove((src + '.tar'))


def copy_some_files(client, src_list, dst):
    """
    Copy multiple files to a Docker container.
    
    Parameters:
        client: Docker client instance
        src_list (list): List of source file paths
        dst (str): Destination container path in format 'container_name:/path'
    """
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src, dst)


def copy_files_V2_windows(src, loc):
    """
    Copy files using Windows Xcopy command.
    
    Parameters:
        src (str): Source file path
        loc (str): Destination directory location
    """
    cmd = "Xcopy " + '"' + src + '"' + " " + '"' + loc + "/I_Raw" + '"' + " /E /H /I"
    print("Executing copy command: ", cmd)
    os.system(cmd)


def process(filepath,drift_val,lc_val,minI_val):
    global client,image,local_mem,command_list
    file_path = filepath
    cont_name = ("PP_container")
    command_list_1[3] = drift_val
    command_list_1[5] = lc_val
    command_list_1[7] = minI_val
    copy_files_V2_windows(file_path, local_mem)
    listy = ["mkdir .\\XXX"]
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/II_Preprocessed', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    PP_container = client.containers.get(cont_name)
    if platform.system().upper() == "DARWIN":
        print("Darwin")
        copy_dst = cont_name + ":/tmp/"
    if platform.system().upper() == "WINDOWS":
        print("Windows")
        copy_dst = cont_name + "C:\\tmp"
        # copy_files_V2_windows(file_path, PP_container, local_mem)
    # copy_a_file(client, file_path,copy_dst)
    # copy_some_files(client, file_path, 'PP_container:/tmp')
    print("Files copied to container: ", cont_name)
    # command_list_1[3] = drift_val
    # command_list_1[5] = lc_val
    # command_list_1[7] = minI_val
    print("PNNL PreProcessor started in container: ",cont_name)
    #PP_container.exec_run(cmd=command_0)
    print("Metadata Extracted. ")
    # for item in command_list_1:
    #     print("cmd list 1 item ", item)
    listy = ["mkdir .\\XXX"]
    PP_container.exec_run(cmd="mkdir test_dir")
    # PP_container.exec_run(cmd=command_list_1)
    print("PNNL PreProcessor completed in container: ", cont_name)
    
    # PP_container.stop()
    # PP_container.remove()

def run_container(raw_file_folder, drift_val, lc_val, minI_val):
    """
    Orchestrate preprocessing of raw ion mobility files.
    
    Note: Current implementation incomplete due to DLL compatibility issues.
    
    Parameters:
        raw_file_folder (str): Path to folder containing raw data files
        drift_val (str): Drift kernel parameter value
        lc_val (str): LC kernel parameter value
        minI_val (str): Minimum intensity threshold value
        
    Returns:
        str: Path to preprocessed data directory
    """
    global client, image, local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    
    local_mem = os.getcwd() + "/II_Preprocessed"
    print("PNNL PreProcessor working directory: ", local_mem)
    os.makedirs("./II_Preprocessed", exist_ok=True)

    return local_mem

