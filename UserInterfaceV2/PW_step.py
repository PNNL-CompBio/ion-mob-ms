#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

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

#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

#Set initial variables,
#Determine local mem
client = docker.from_env()
image = "anubhav0fnu/proteowizard"    

# command_list = ["wine", "msconvert", "--zlib", "-e",".mzML.gz","-o","/III_mzML", "placeholder"]

#This is the command that will be run in the container
#Wine is used because Proteowizard/msconvert is a windows tool.
command_list = ["wine64_anyuser", "msconvert", "-e",".mzML","-o","/III_mzML", "placeholder"]


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
    global client,image,local_mem,command_list,save_mem
    file_path = str(filepath.absolute())
    cont_name = ("PW_container_" + os.path.basename(file_path))
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, detach=True, tty=True)
    time.sleep(1)
    print("Container started: ", cont_name)
    PW_container = client.containers.get(cont_name)
    shutil.copytree(file_path,os.path.join(local_mem,os.path.basename(file_path)))
    
    print("Files copied to container: ", cont_name)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    print("Proteowizard msconvert started in container: ",cont_name)
    time.sleep(1)
    PW_container.exec_run(cmd=command_list)
    print("Proteowizard completed in container: ", cont_name)

    time.sleep(1)
    ##
    current_loc = (os.path.join(local_mem,os.path.basename(file_path)))
    shutil.rmtree(current_loc, onerror=onerror)
    print(os.path.basename(file_path), ": shutil")
    current_loc = current_loc[:-2] + ".mzML"
    mv_loc = (os.path.join(save_mem,os.path.basename(file_path)))
    mv_loc = mv_loc[:-2] + ".mzML"
    Path(current_loc).rename(mv_loc)
    print(os.path.basename(file_path), ": rename")
    ##
    time.sleep(1)
    PW_container.stop()
    time.sleep(2)
    PW_container.remove()
    time.sleep(1)
    
    
    
def run_container(raw_file_folder,III_mzML_loc,exptype):
    global client,image,local_mem,command_list,save_mem
    
    save_mem = III_mzML_loc
    local_mem = III_mzML_loc + "_tmp"
    print("ProteoWizard Working Directory: ", local_mem)
    os.makedirs(save_mem, exist_ok = True)
    if os.path.exists(local_mem):
        shutil.rmtree(local_mem)
    os.makedirs(local_mem, exist_ok = True)

    file_list = list(pathlib.Path(raw_file_folder).glob('*'))

    #If Single field data is not Singlefield (determined by suffix), this will do something.
    if exptype == "Single":
        print('Note: Running Single-Field Workflow, any files that do not contain ms1 data will be removed.')
        filtered_files =[]
        for item in file_list:
            ms_level = "no_suffix"
            raw_item = "{}".format(item)
            try:
                print("raw_item is:", raw_item)
                ms_level = re.search(r'\_([0-9]+)\.d', raw_item).group(1)
                print("ms level of ", raw_item, " is ", ms_level)
            except:
                pass
            if ms_level == "1" or ms_level == "no_suffix":
                filtered_files.append(item)
            else:
                print("File not included due to ms level indicated by naming suffix (..._2-#).d,: ", item)
        file_list = filtered_files

    # TODO conditionally execute based on config?
    # Build a dict of all files in unprocessed-directory of
    #   KEY: <filename no suffix>
    #   VALUE: a tuple of (<filepath>, <filename suffix>)
    raw_files_no_ext_map = {Path(file).with_suffix('').name: (file, Path(file).suffix) for file in file_list}
    # Get list of already processed file
    file_list_processed = list(pathlib.Path(save_mem).glob('*'))
    # Build a dict of all files in already-processed-directory of
    #   KEY: <filename without suffix>
    #   VALUE: a tuple of (filepath, suffix)
    processed_files_no_ext_map = {Path(file).absolute().with_suffix('').name: (file, Path(file).suffix) for file in file_list_processed}
    # find the difference in processed and unprocessed sets built from the keys of both dicts
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    # transform difference list of kvps back into list of unprocessed filepaths of type pathlib.Path
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'found unprocessed files count: {len(file_list)}')
    #This limits containers to 10 at a time. This is important for running locally.
    #If this ever hits the cloud, "the limit does not exist!"
    #This generates subprocesses - each subprocess runs a container which runs one file.
    process_num = len(file_list)
    
    cpu_count = os.cpu_count()
    if cpu_count > 6:
        cpu_count -= 2

    if process_num > cpu_count:
        process_num = cpu_count

    if process_num == 0:
        return save_mem
    pool = Pool(processes=process_num)

    for _ in tqdm.tqdm(pool.imap(process, file_list), total=len(file_list)):
        pass

    pool.close()
    pool.join()
    shutil.rmtree(local_mem)
    return save_mem

