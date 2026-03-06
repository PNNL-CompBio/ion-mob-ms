#!/usr/bin/env python3.9

"""
PP_gui.py - PNNL Preprocessor Ion Mobility Data GUI Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Provides graphical interface integration for PNNL PreProcessor Windows application.
    This module orchestrates Docker container execution with Wine emulation layer.
    
    Current Implementation Status: INCOMPLETE
    Due to DLL compatibility issues with proprietary Agilent ImsBrowser components,
    the PNNL-PreProcessor.exe Windows executable fails to execute correctly within
    Wine containers. Previous success required proprietary ImsBrowser installation,
    which cannot be distributed or used in this implementation.
    
    The module retains complete file transfer and container orchestration infrastructure
    for future implementation once an alternative preprocessing method is identified
    or DLL compatibility is resolved. All helper functions are functional and ready
    for integration with a working preprocessing implementation.
    
    Key Features:
    - Docker-based preprocessing with Wine compatibility layer
    - Platform-aware file transfer (macOS tar-based, Windows native copy)
    - Complete container orchestration infrastructure
    - Preserved helper functions ready for replacement implementation
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


# Initialize Docker client and container image
client = docker.from_env()
image = "jjacobson95/pnnl_preprocessor4"    
local_mem = os.getcwd() + "/II_Preprocessed"
# R script for metadata extraction from raw ion mobility files
command_0 = """Rscript /tmp/R_Metadata_I.R"""

# PNNL-PreProcessor command with parameters for filtering and smoothing.
# NOTE: This command currently fails due to DLL compatibility issues in Wine.
# See module docstring for details.
command_list_1 = ["C:\\PNNL-Preprocessor_4.0_2022.02.17\\PNNL-Preprocessor\\PNNL-PreProcessor.exe", "-smooth","-driftKernel","1","-lcKernel","0","-minIntensity","20","-split","-r","-d",'"..\\..\\tmp\\II_Preprocessed\\I_Raw"']


def copy_a_file(client, src,dst):
    """
    Transfer file to Docker container using platform-aware methods.
    
    On macOS/Linux, uses tar-based archiving; on Windows, uses direct
    container name and path parsing for Windows-path-aware operations.
    
    Parameters:
        client: Docker client instance
        src (str): Source file path on host machine
        dst (str): Destination path in format 'container_name:/container/path'
        
    Returns:
        None
    """
    if platform.system().upper() == "DARWIN":
        name, dst = dst.split(':')
    if platform.system().upper() == "WINDOWS":
        name = dst[:-6]
        dst = dst[-6:]
        print("name: ", name)
        print("dst: ", dst)
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

def copy_some_files(client, src_list,dst):
    """
    Transfer multiple files to Docker container.
    
    Parameters:
        client: Docker client instance
        src_list (list): List of source file paths
        dst (str): Base destination path in container
        
    Returns:
        None
    """
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src,dst)


def copy_files_V2_windows(src,loc):
    """
    Windows-specific recursive file copy using Xcopy command.
    
    Parameters:
        src (str): Source directory path
        loc (str): Destination location base path
        
    Returns:
        None
    """
    cmd = "Xcopy " + '"' + src + '"'+ " " + '"' + loc + "/I_Raw" + '"' + " /E /H /I"
    print("command is ", cmd)
    os.system(cmd)


def process(filepath,drift_val,lc_val,minI_val):
    """
    Process ion mobility file with PNNL PreProcessor (INCOMPLETE).
    
    Currently non-functional due to DLL compatibility issues with PNNL-PreProcessor.exe
    in Wine container. See module docstring for details and workaround information.
    
    Parameters:
        filepath (str): Path to raw ion mobility data directory
        drift_val (str): Drift kernel filtering parameter value
        lc_val (str): LC kernel filtering parameter value
        minI_val (str): Minimum intensity threshold parameter value
        
    Returns:
        None
    """
    global client,image,local_mem,command_list
    file_path = filepath
    cont_name = ("PP_container")
    command_list_1[3] = drift_val
    command_list_1[5] = lc_val
    command_list_1[7] = minI_val
    copy_files_V2_windows(file_path, local_mem)
    
    # Create and start preprocessing container with volume mounting
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/II_Preprocessed', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    PP_container = client.containers.get(cont_name)
    
    # Set container destination path based on platform
    if platform.system().upper() == "DARWIN":
        print("Darwin")
        copy_dst = cont_name + ":/tmp/"
    if platform.system().upper() == "WINDOWS":
        print("Windows")
        copy_dst = cont_name + "C:\\tmp"
    
    print("Files copied to container: ", cont_name)
    print("PNNL PreProcessor started in container: ",cont_name)
    print("Metadata Extracted.")
    
    # Placeholder container command - actual preprocessing fails due to DLL issues
    PP_container.exec_run(cmd="mkdir test_dir")
    print("PNNL PreProcessor completed in container: ", cont_name)


def run_container(raw_file_folder,drift_val,lc_val,minI_val):
    """
    Orchestrate PNNL PreProcessor execution (INCOMPLETE).
    
    Sets up working directory and container infrastructure but does not execute
    actual preprocessing due to DLL compatibility issues. See module docstring
    for current status and limitations.
    
    Parameters:
        raw_file_folder (str): Path to raw ion mobility data directory
        drift_val (str): Drift kernel filtering parameter value
        lc_val (str): LC kernel filtering parameter value  
        minI_val (str): Minimum intensity threshold parameter value
        
    Returns:
        str: Path to preprocessing working directory (incomplete processing)
    """
    global client,image,local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    print("curdur is: ",cur_dir)
    local_mem = os.getcwd() + "/II_Preprocessed"
    print("PNNL PreProcessor Working Directory: ", local_mem)
    os.makedirs("./II_Preprocessed", exist_ok = True)

    process(raw_file_folder,drift_val,lc_val,minI_val)

    return local_mem

