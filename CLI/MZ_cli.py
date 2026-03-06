#!/usr/bin/env python3.9
"""
MZ_cli.py - MZmine Feature Detection Command Line Interface Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides command-line interface functionality for the MZmine2 feature detection tool.
    It orchestrates Docker container execution for detecting features in mzML data files using MZmine.
    Implements parallel processing with intelligent resource management.
    
    Key Features:
    - Docker container orchestration for MZmine batch processing
    - Parallel processing with CPU and memory-aware process limiting
    - Incremental processing (skips already-processed files)
    - XML batch file template modification for each file
    - Progress tracking with tqdm
    - Cross-platform file handling
    - Timestamps for all operations
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
import tqdm
from datetime import datetime
from functools import partial
import psutil


# Runtime logging with timestamps for execution tracking
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

client = docker.from_env()
image = "anubhav0fnu/mzmine:latest"

# MZmine batch processing command for Linux containers
command_list_2 = ["bash", "startMZmine_Linux.sh", "/tmp/MZmine_FeatureFinder-batch.xml"]



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
    Process a single mzML file through MZmine feature detection in a Docker container.
    
    Parameters:
        filepath: Path to mzML file to process
    """
    global client, image, local_mem, save_mem, command_list_2
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("MZ_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    client.containers.run(image, name=cont_name, volumes={local_mem: {'bind': '/tmp/IV_Features_csv', 'mode': 'rw'}}, 
                         detach=True, tty=True)
    print("Container started: ", cont_name)
    MZ_container = client.containers.get(cont_name)

    # Modify template XML file with current input file name using sed
    command_list_1 = """sed -i 's/REPLACE_THIS_LINE/        <parameter name="Raw data file names"><file>\/tmp\/III_mzML\/""" + file_name + """<\/file><\/parameter>/' /tmp/MZmine_FeatureFinder-batch.xml"""
    copy_dst = cont_name + ":/tmp/III_mzML/"
    copy_a_file(client, file_path, copy_dst)
    command_list_0 = """Rscript /tmp/R_PARSE_II.R"""
    print("Files copied to container: ", cont_name)
    print("MZmine feature detection started in container: ", cont_name)
    MZ_container.exec_run(cmd=command_list_0)
    MZ_container.exec_run(cmd=command_list_1)
    MZ_container.exec_run(cmd=command_list_2)
    print("MZmine feature detection completed in container: ", cont_name)
    
    # Move processed file to output directory
    current_loc = (os.path.join(local_mem, os.path.basename(file_path)))
    current_loc = current_loc + "_c_dc_de.csv"
    mv_loc = (os.path.join(save_mem, os.path.basename(file_path)))
    mv_loc = mv_loc + "_c_dc_de.csv"
    Path(current_loc).rename(mv_loc)

    MZ_container.stop()
    time.sleep(2)
    MZ_container.remove()
    return

#def check_memory_and_start_thread(arg):
 #   target_memory_limit = 4 * 1024 * 1024 * 1024 # 4 Gb
  #  available_memory = psutil.virtual_memory().free 
   # while available_memory < target_memory_limit:
    #    time.sleep(1)  # Wait for 1 second before checking again
     #   available_memory = psutil.virtual_memory().free
#    return process(arg)

def run_container(mzML_data_folder, Feature_data_loc):
    """
    Orchestrate batch processing of mzML files through MZmine feature detection.
    Implements intelligent parallel processing with CPU and memory constraints.
    
    Parameters:
        mzML_data_folder (str): Path to folder containing mzML input files
        Feature_data_loc (str): Output directory for feature CSV files
        
    Returns:
        str: Path to temporary working directory
    """
    global client, image, local_mem, save_mem, command_list_2
    
    save_mem = Feature_data_loc
    local_mem = Feature_data_loc + "_tmp"
    
    os.makedirs(save_mem, exist_ok=True)
    if os.path.exists(local_mem):
        shutil.rmtree(local_mem)
    os.makedirs(local_mem, exist_ok=True)
    
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))

    # Build index of unprocessed files by comparing input and output directories
    raw_files_no_ext_map = {Path(file).with_suffix('').name: (file, Path(file).suffix) for file in file_list}
    file_list_processed = list(pathlib.Path(save_mem).glob('*'))
    processed_files_no_ext_map = {os.path.basename(os.path.splitext(os.path.splitext(Path(file).absolute())[0])[0]): 
                                  (file, "".join(Path(file).suffixes)) for file in file_list_processed}
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'Found unprocessed files count: {len(file_list)}')
    
    # Determine optimal number of parallel processes based on CPU count and available memory
    process_num = len(file_list)   
    cpu_count = os.cpu_count()
    if process_num > cpu_count - 2:
        process_num = cpu_count - 2

    if process_num > (psutil.virtual_memory().available // (1000000000 * 2.5)): 
        process_num = int(psutil.virtual_memory().available // (1000000000 * 2.5))
    if process_num == 0:
        return save_mem
    
    print("Maximum parallel processes determined: ", process_num) 
    pool = Pool(processes=process_num)
    
    for _ in tqdm.tqdm(pool.imap(process, file_list), total=len(file_list)):
        pass

    pool.close()
    pool.join()
    
    shutil.rmtree(local_mem)
    return local_mem
