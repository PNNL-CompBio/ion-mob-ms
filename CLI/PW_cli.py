#!/usr/bin/env python3.9
"""
PW_cli.py - Proteowizard/msconvert Command Line Interface Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module provides command-line interface functionality for the Proteowizard/msconvert tool.
    It orchestrates Docker container execution for converting raw ion mobility data to mzML format.
    Implements parallel processing with intelligent resource management.
    
    Key Features:
    - Docker container orchestration for Proteowizard msconvert
    - Parallel batch processing of raw data files
    - Incremental processing (skips already-converted files)
    - Cross-platform file handling (Windows, macOS, Linux)
    - Memory and CPU-aware process limiting
    - Progress tracking with tqdm
    - Timestamps for all operations
    
Note:
    - Uses Wine64 to execute Windows-based msconvert executable
    - Parallel processing is limited by available system resources
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
import re
from pathlib import Path
import shutil
import glob
import tqdm
from datetime import datetime
import psutil


# Runtime logging with timestamps for execution tracking
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

# Initialize Docker client and image
client = docker.from_env()
image = "anubhav0fnu/proteowizard"    

# msconvert command: convert raw files to mzML format
command_list = ["wine64_anyuser", "msconvert", "-e", ".mzML", "-o", "/III_mzML", "placeholder"]


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def process(filepath):
    """
    Convert a single raw data file to mzML format in a Docker container.
    
    Parameters:
        filepath: Path to raw data file (e.g., .d directory from Agilent)
    """
    global client, image, local_mem, command_list, save_mem
    file_path = str(filepath.absolute())
    cont_name = ("PW_container_" + os.path.basename(file_path))
    client.containers.run(image, name=cont_name, volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, 
                         detach=True, tty=True)
    time.sleep(1)
    print("Container started: ", cont_name)
    PW_container = client.containers.get(cont_name)
    shutil.copytree(file_path, os.path.join(local_mem, os.path.basename(file_path)))
    
    print("Files copied to container: ", cont_name)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    print("Proteowizard msconvert started in container: ", cont_name)
    time.sleep(1)
    PW_container.exec_run(cmd=command_list)
    print("Proteowizard conversion completed in container: ", cont_name)

    time.sleep(1)
    # Clean up input directory and move output to results directory
    current_loc = (os.path.join(local_mem, os.path.basename(file_path)))
    shutil.rmtree(current_loc, onerror=onerror)
    print(os.path.basename(file_path), ": input directory removed")
    current_loc = current_loc[:-2] + ".mzML"
    mv_loc = (os.path.join(save_mem, os.path.basename(file_path)))
    mv_loc = mv_loc[:-2] + ".mzML"
    Path(current_loc).rename(mv_loc)
    print(os.path.basename(file_path), ": file moved to output directory")
    
    PW_container.stop()
    time.sleep(2)
    PW_container.remove()
    time.sleep(1)
    
    
    
def run_container(raw_file_folder, III_mzML_loc, exptype):
    """
    Orchestrate batch conversion of raw data files to mzML format.
    Implements intelligent parallel processing with CPU and memory constraints.
    
    Parameters:
        raw_file_folder (str): Path to folder containing raw data files
        III_mzML_loc (str): Output directory for mzML files
        exptype (str): Experiment type (e.g., 'Single') for filtering file set
        
    Returns:
        str: Path to mzML output directory
    """
    global client, image, local_mem, command_list, save_mem
    
    save_mem = III_mzML_loc
    local_mem = III_mzML_loc + "_tmp"
    print("ProteoWizard working directory: ", local_mem)
    os.makedirs(save_mem, exist_ok=True)
    if os.path.exists(local_mem):
        shutil.rmtree(local_mem)
    os.makedirs(local_mem, exist_ok=True)

    file_list = list(pathlib.Path(raw_file_folder).glob('*'))

    # Filter files based on experiment type to remove non-MS1 data
    if exptype == "Single":
        print('Single-field workflow: filtering files to include only MS1 data.')
        filtered_files = []
        for item in file_list:
            ms_level = "no_suffix"
            raw_item = "{}".format(item)
            try:
                print("Checking file: ", raw_item)
                ms_level = re.search(r'_([0-9]+)\.d', raw_item).group(1)
                print("MS level of ", raw_item, " is ", ms_level)
            except:
                pass
            if ms_level == "1" or ms_level == "no_suffix":
                filtered_files.append(item)
            else:
                print("File excluded due to MS level suffix: ", item)
        file_list = filtered_files

    # Build index of unprocessed files
    raw_files_no_ext_map = {Path(file).with_suffix('').name: (file, Path(file).suffix) for file in file_list}
    file_list_processed = list(pathlib.Path(save_mem).glob('*'))
    processed_files_no_ext_map = {Path(file).absolute().with_suffix('').name: (file, Path(file).suffix) 
                                  for file in file_list_processed}
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'Found unprocessed files count: {len(file_list)}')
    
    # Determine optimal number of parallel processes
    process_num = len(file_list)
    cpu_count = os.cpu_count()
    if cpu_count > 6:
        cpu_count -= 2

    if process_num > (cpu_count - 2):
        process_num = (cpu_count - 2)
        
    if process_num > (psutil.virtual_memory().available // (1000000000 * 2.2)): 
        process_num = int(psutil.virtual_memory().available // (1000000000 * 2.2))

    if process_num == 0:
        return save_mem
    
    print("Maximum parallel processes determined: ", process_num) 
    pool = Pool(processes=process_num)

    for _ in tqdm.tqdm(pool.imap(process, file_list), total=len(file_list)):
        pass

    pool.close()
    pool.join()
    shutil.rmtree(local_mem)
    return save_mem

