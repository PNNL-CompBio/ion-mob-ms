#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import sys
import os
import tarfile
import time
import platform
import pathlib
import threading
from multiprocessing import Pool
import io
import re
from spython.main import Client
import glob
from pathlib import Path
import shutil
import glob
import tqdm
from datetime import datetime

#Set initial variables,
#Determine local mem

old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

#Set initial variables,
#Determine local mem

local_mem = os.path.join(os.getcwd(),"III_mzML_tmp")
save_mem = os.path.join(os.getcwd(),"III_mzML")

#This is the command that will be run in the container
#Wine is used because Proteowizard/msconvert is a windows tool.

command_list = ["wine64", "msconvert", "-e",".mzML","-o","/III_mzML", "placeholder"]


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
    global image,local_mem,command_list,save_mem
    file_path = str(filepath.absolute())

    options = ["--bind", local_mem +":/III_mzML"]
    myinstance = Client.instance('./proteowizard.sandbox', options=options)
    PW_container = myinstance.name

    time.sleep(1)
    print("Container started: ", PW_container)
    
    PW_container = myinstance.name
    

    shutil.copytree(file_path,os.path.join(local_mem,os.path.basename(file_path)))
    
    print("Files copied to container: ", PW_container)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    print("Proteowizard msconvert starting in container: ",PW_container)
    time.sleep(1)

    Client.execute(myinstance,command_list)

    print("Proteowizard completed in container: ", PW_container)

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
    time.sleep(1)
    myinstance.stop()
    time.sleep(1)
    
    
    
def run_container(raw_file_folder,exptype):
    global image,local_mem,command_list,save_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.path.join(os.getcwd(),"III_mzML_tmp")
    save_mem = os.path.join(os.getcwd(),"III_mzML")
    print("ProteoWizard Working Directory: ", local_mem)
    os.makedirs("./III_mzML", exist_ok = True)
    os.makedirs("./III_mzML_tmp", exist_ok = True)

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
    file_list_processed = list(pathlib.Path("./III_mzML").glob('*'))
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
    if process_num > 4:
        process_num = 4

    if process_num == 0:
        return save_mem
    pool = Pool(processes=process_num)

    for _ in tqdm.tqdm(pool.imap(process, file_list), total=len(file_list)):
        pass

    pool.close()
    pool.join()
    shutil.rmtree(local_mem)
    return save_mem
