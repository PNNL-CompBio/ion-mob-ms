#!/usr/bin/env python3.7

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
import random
import string


#Set initial variables,
#Determine local mem
 
#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")

save_mem = os.path.join(os.getcwd(),"IV_Features_csv")

def process(input_args):
    global image,local_mem,command_list,save_mem
    filepath = input_args[0]
    tmp_mount =  input_args[1]
    tmp_mount_mem = os.path.join(os.getcwd(),"IV_Features_tmp_mount",tmp_mount)
    os.makedirs(tmp_mount_mem, exist_ok=True)
    file_path = str(filepath.absolute())
    file_name = os.path.basename(file_path)
    options = ["--writable-tmpfs","--bind", local_mem + ":/Work/III_mzML", "--bind", tmp_mount_mem+":/Work/tmp"]
    # options = ["--bind", "/vagrant/dev_dockerized/drf/backend/mzMLData:/home/vagrant"]
    myinstance = Client.instance('./mzmine_updated.sif', options=options)
    MZ_container = myinstance.name
        
    command_list_0 = """Rscript /Work/R_PARSE_II.R"""
# doesnt work    command_list_0 = """Rscript /Work/R_PARSE_II.R ParseDTasRTmzML 1 /Work/III_mzML/""" + file_name
#    command_list_0 = """Rscript -e 'source("R_PARSE_II.R"); ParseDTasRTmzML(1,"/Work/III_mzML/""" + file_name + """")'"""    
    command_list_1 = """python MZmine_FeatureFinder_Modifier.py -n """ + file_name
    command_list_2 = """bash /MZmine-2.41.2/startMZmine_Linux.sh /Work/MZmine_FeatureFinder-batch.xml"""
    print("command_list_1:", command_list_1)

    shutil.copy(file_path, os.path.join(local_mem))

    Client.execute(myinstance,command_list_1, options=['--writable-tmpfs'],quiet=False)
    Client.execute(myinstance,command_list_0, options=['--writable-tmpfs'],quiet=False)
    
##    shutil.copy(file_path, os.path.join(local_mem))

    Client.execute(myinstance,command_list_2, options=['--writable-tmpfs'],quiet=False)

    print("Instance complete: ",myinstance,"   ",filepath)
    current_loc = (os.path.join(local_mem,os.path.basename(file_path)))
    current_loc = current_loc + "_c_dc_de.csv"
    mv_loc = (os.path.join(save_mem,os.path.basename(file_path)))
    mv_loc = mv_loc + "_c_dc_de.csv"
    Path(current_loc).rename(mv_loc)

    myinstance.stop()
    time.sleep(2)

def run_container(mzML_data_folder,Feature_data_loc):
    global local_mem, save_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")
    save_mem = os.path.join(os.getcwd(),"IV_Features_csv")
    
    save_mem = Feature_data_loc
    local_mem = Feature_data_loc + "_tmp"
    # os.makedirs("./IV_Features_csv_tmp", exist_ok=True)
    # os.makedirs("./IV_Features_csv", exist_ok=True)
    os.makedirs(save_mem, exist_ok = True)
    if os.path.exists(local_mem):
        shutil.rmtree(local_mem)
    os.makedirs(local_mem, exist_ok = True)
    
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))


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
    processed_files_no_ext_map = {os.path.basename(os.path.splitext(os.path.splitext(Path(file).absolute())[0])[0]): (file, "".join(Path(file).suffixes)) for file in file_list_processed}
    # find the difference in processed and unprocessed sets built from the keys of both dicts
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    # transform difference list of kvps back into list of unprocessed filepaths of type pathlib.Path
    
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'found unprocessed files count: {len(file_list)}')
    
    
    
    
    # Generate a list of unique strings
    N = len(file_list)
    string_length = 5
    random_strings = []
    while len(random_strings) < N:
        # Generate a random string
        new_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(string_length))
        # Check if it's already in the list
        if new_string not in random_strings:
            random_strings.append(new_string)
    process_args = zip(file_list, random_strings)    
    
    process_num = len(file_list)
    
    if process_num > os.cpu_count():
        process_num = os.cpu_count()

    if process_num == 0:
        return local_mem
    
    pool = Pool(processes=process_num)
    # pool.map(process, file_list)

    for _ in tqdm.tqdm(pool.imap(process, process_args), total=len(file_list), leave=None):
            pass

    pool.close()
    pool.join()
    return local_mem


