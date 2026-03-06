#!/usr/bin/env python3.9

"""
MZ_gui.py - MZmine Batch Feature Detection GUI Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Provides graphical interface integration for MZmine batch processing of mzML
    spectral data files. This module orchestrates Docker container execution of
    MZmine feature detection with configuration template modification on a per-file
    basis. Implements intelligent parallel processing with CPU-aware process
    limiting to prevent resource exhaustion on workstation hardware.
    
    Key Features:
    - Docker-based MZmine execution with persistent volume mounting
    - Per-file XML configuration template modification using sed commands
    - Incremental processing to skip already-processed files
    - CPU-aware parallel processing with configurable process limits
    - Cross-platform file transfer using tar-based Docker archive methods
    - Timestamp-stamped logging for execution tracking
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
from pathlib import Path
import stat
import shutil
from datetime import datetime

# Container runtime logging with timestamps
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print
local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")
save_mem = os.path.join(os.getcwd(),"IV_Features_csv") 
client = docker.from_env()
image = "anubhav0fnu/mzmine:latest"

# MZmine execution command for Docker container environment.
# Runs bash initialization script followed by feature detection on configured XML batch file.
command_list_2 = ["bash", "startMZmine_Linux.sh", "/tmp/MZmine_FeatureFinder-batch.xml"]

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
    Process individual mzML file through MZmine feature detection.
    
    Creates isolated Docker container for each file, modifies XML configuration
    template with file-specific path, runs MZmine feature detection, and moves
    results to permanent storage location.
    
    Parameters:
        filepath (Path): Pathlib Path object to mzML file
        
    Returns:
        None
    """
    global client,image,local_mem,save_mem,command_list_2
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("MZ_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/IV_Features_csv', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    MZ_container = client.containers.get(cont_name)

    #This line is required to modify the template xml file.
    command_list_1 = """sed -i 's/REPLACE_THIS_LINE/        <parameter name="Raw data file names"><file>\/tmp\/III_mzML\/""" +file_name + """<\/file><\/parameter>/' /tmp/MZmine_FeatureFinder-batch.xml"""
    copy_dst = cont_name + ":/tmp/III_mzML/"
    # shutil.copy(file_path, os.path.join(local_mem))
    copy_a_file(client, file_path,copy_dst)
    command_list_0 = """Rscript /tmp/R_PARSE_II.R"""
    print("Files copied to container: ", cont_name)
    print("MzMine started in container: ",cont_name)
    MZ_container.exec_run(cmd=command_list_0)
    MZ_container.exec_run(cmd=command_list_1)
    MZ_container.exec_run(cmd=command_list_2)
    print("MzMine completed in container: ", cont_name)
    
    # Move processed feature CSV from temporary to permanent storage location
    current_loc = (os.path.join(local_mem,os.path.basename(file_path)))
    current_loc = current_loc + "_c_dc_de.csv"
    mv_loc = (os.path.join(save_mem,os.path.basename(file_path)))
    mv_loc = mv_loc + "_c_dc_de.csv"
    Path(current_loc).rename(mv_loc)

    # Clean up container resources
    MZ_container.stop()
    time.sleep(2)
    MZ_container.remove()


def run_container(mzML_data_folder):
    """
    Orchestrate batch MZmine processing of mzML files with parallel execution.
    
    Creates working directories, identifies unprocessed files by comparing input
    directory against output directory, and processes files in parallel constrained
    by available CPU cores. Implements intelligent skipping of already-processed
    files to enable incremental processing.
    
    Parameters:
        mzML_data_folder (str): Path to directory containing mzML spectral files
        
    Returns:
        str: Path to directory containing feature detection results
    """
    global client,image,local_mem,save_mem,command_list_2
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)    
    os.makedirs(save_mem, exist_ok = True)
    if os.path.exists(local_mem):
        shutil.rmtree(local_mem)
    os.makedirs(local_mem, exist_ok = True)
    
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))

    # Identify already-processed files to enable incremental processing.
    # Build dictionary mapping filenames (without suffix) to their full paths.
    raw_files_no_ext_map = {Path(file).with_suffix('').name: (file, Path(file).suffix) for file in file_list}
    
    # Get list of already processed files from output directory
    file_list_processed = list(pathlib.Path(save_mem).glob('*'))
    
    # Build dictionary of processed files for comparison
    processed_files_no_ext_map = {os.path.basename(os.path.splitext(os.path.splitext(Path(file).absolute())[0])[0]): (file, "".join(Path(file).suffixes)) for file in file_list_processed}
    
    # Find files that have not yet been processed
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    
    # Convert filename list back to full filepath list
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'found unprocessed files count: {len(file_list)}')
    
    # Constrain parallelization to available CPU cores minus safety margin
    process_num = len(file_list)    
    cpu_count = os.cpu_count()
    if cpu_count > 6:
        cpu_count -= 2

    if process_num > cpu_count:
        process_num = cpu_count

    # Return immediately if no unprocessed files found
    if process_num == 0:
        return local_mem
    
    # Execute feature detection in parallel using worker process pool
    pool = Pool(processes=process_num)
    pool.imap(process, file_list)
    pool.close()
    pool.join()
    
    # Clean up temporary working directory
    shutil.rmtree(local_mem)
    return save_mem
