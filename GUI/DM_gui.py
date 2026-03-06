#!/usr/bin/env python3.9

"""
DM_gui.py - Deimos Persistent Homology Feature Detection GUI Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Provides graphical interface integration for Deimos persistent homology-based
    feature detection for ion mobility mass spectrometry data. This module orchestrates
    Docker container execution with per-file isolation and configurable memory limits.
    Due to container resource constraints, parallelization is strictly limited to
    3 concurrent processes to maintain stability and prevent processing failures.
    
    Key Features:
    - Docker-based Deimos execution with 14GB memory limit per container
    - Tar-based file transfer for cross-platform Docker volume mounting
    - Hard-limited parallelization (max 3 processes) for container stability
    - Timestamp-stamped logging for execution tracking
    
Known Limitations:
    Deimos performance is currently slower than expected due to container resource
    constraints. Increasing parallelization beyond 3 processes results in regular
    processing failures. Future optimization may improve execution speed.
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
image = "anubhav0fnu/ccs_comparison"
local_mem = os.getcwd() + "/IV_Features_csv"

def copy_a_file(client, src,dst):
    """
    Transfer file to Docker container using tar-based archive method.
    
    Parameters:
        client: Docker client instance
        src (str): Source file path on host machine
        dst (str): Destination path in format 'container_name:/container/path'
        
    Returns:
        None
    """
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


def process(filepath):
    """
    Process individual mzML file through Deimos feature detection.
    
    Creates isolated Docker container for each file with 14GB memory limit,
    transfers file, executes Deimos feature detection, and cleans up resources.
    
    Parameters:
        filepath (Path): Pathlib Path object to mzML file
        
    Returns:
        None
    """
    global client,image,local_mem
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("DM_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    # Container memory limit of 14GB per process; increase if memory errors occur
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/IV_Features_csv', 'mode': 'rw'}}, mem_limit="14g",detach=True, tty=True)
    print("Container started: ", cont_name)
    DM_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    print("Files copied to container: ", cont_name)
    print("Deimos started in container: ",cont_name)
    DM_container.exec_run(cmd="python /tmp/deimos_feature_finder.py")
    print("Deimos completed in container: ", cont_name)
    time.sleep(1)
    DM_container.stop()
    time.sleep(2)
    DM_container.remove()

def run_container(mzML_data_folder):
    """
    Orchestrate batch Deimos feature detection with limited parallelization.
    
    Creates working directory, identifies files to process, and executes Deimos
    feature detection in strictly limited parallel execution (max 3 processes).
    This limitation is necessary to maintain container stability with current
    Docker resource constraints.
    
    Parameters:
        mzML_data_folder (str): Path to directory containing mzML spectral files
        
    Returns:
        str: Path to directory containing feature detection results
    """
    global client,image,local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    local_mem = os.getcwd() + "/IV_Features_csv"
    print("Deimos Working Directory: ", local_mem)
    os.makedirs("./IV_Features_csv", exist_ok=True)
    
    # Locate all unprocessed mzML files
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))

    # Hard-limit parallelization to 3 processes for stability.
    # Higher process counts result in consistent container failures.
    process_num = len(file_list)
    if process_num > 3:
        process_num = 3
    
    # Execute feature detection in parallel within process limit
    pool = Pool(processes=process_num)
    pool.map(process, file_list)
    pool.close()
    pool.join()
    return local_mem