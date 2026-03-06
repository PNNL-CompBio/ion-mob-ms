#!/usr/bin/env python3.9
"""
DM_cli.py - Deimos Feature Detection Command Line Interface Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides command-line interface functionality for the Deimos feature detection tool.
    It orchestrates Docker container execution for detecting features in mzML ion mobility data files.
    Deimos performs feature picking using persistent homology algorithms.
    
    Key Features:
    - Docker container management for Deimos execution
    - Batch processing of mzML files with parallel processing
    - File staging and result retrieval
    - Automatic memory management with container resource limits
    - Cross-platform file handling
    
    Note:
    - Performance is currently limited by container resource constraints
    - Parallel processing is limited to 3 processes maximum for stability
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
image = "anubhav0fnu/ccs_comparison"
local_mem = os.getcwd() + "/IV_Features_csv"


def copy_a_file(client, src, dst):
    """
    Copy a file to a Docker container using tar archive.
    
    Parameters:
        client: Docker client instance
        src (str): Source file path on host
        dst (str): Destination in container format 'container_name:/path'
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


def process(filepath):
    """
    Process a single mzML file through Deimos feature detection in a Docker container.
    
    Parameters:
        filepath: Path to mzML file to process
    """
    global client, image, local_mem
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("DM_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    # Run container with memory limit to prevent resource exhaustion
    client.containers.run(image, name=cont_name, volumes={local_mem: {'bind': '/IV_Features_csv', 'mode': 'rw'}}, 
                         mem_limit="14g", detach=True, tty=True)
    print("Container started: ", cont_name)
    DM_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/III_mzML/"
    copy_a_file(client, file_path, copy_dst)
    print("Files copied to container: ", cont_name)
    print("Deimos feature detection started in container: ", cont_name)
    DM_container.exec_run(cmd="python /tmp/deimos_feature_finder.py")
    print("Deimos feature detection completed in container: ", cont_name)
    time.sleep(1)
    DM_container.stop()
    time.sleep(2)
    DM_container.remove()

def run_container(mzML_data_folder):
    """
    Orchestrate batch processing of mzML files through Deimos feature detection.
    
    Parameters:
        mzML_data_folder (str): Path to folder containing mzML files
        
    Returns:
        str: Path to output directory with feature CSV files
    """
    global client, image, local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    local_mem = os.getcwd() + "/IV_Features_csv"
    print("Deimos working directory: ", local_mem)
    os.makedirs("./IV_Features_csv", exist_ok=True)
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))

    # Limit parallel processes to 3 for stability with container resources
    process_num = len(file_list)
    if process_num > 3:
        process_num = 3
        
    pool = Pool(processes=process_num)
    pool.map(process, file_list)

    pool.close()
    pool.join()
    return local_mem