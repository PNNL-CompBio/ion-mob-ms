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
from pathlib import Path
import stat
import shutil
import tqdm
from datetime import datetime

#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

client = docker.from_env()
image = "anubhav0fnu/mzmine:latest"
local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")
save_mem = os.path.join(os.getcwd(),"IV_Features_csv")


#This is the command line usage. Nice and simple. Must be run from the MZmine folder. This is in linux!!
#It first requires modification of a xml batch file (below with sed).
command_list_2 = ["bash", "startMZmine_Linux.sh", "/tmp/MZmine_FeatureFinder-batch.xml"]

#Copy file functions
#if mac
def copy_a_file(client, src,dst):
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
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src,dst)


def process(filepath):
    global client,image,local_mem,command_list_2
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
    
    current_loc = (os.path.join(local_mem,os.path.basename(file_path)))
    current_loc = current_loc + "_c_dc_de.csv"
    mv_loc = (os.path.join(save_mem,os.path.basename(file_path)))
    mv_loc = mv_loc + "_c_dc_de.csv"
    # os.chmod(current_loc,stat.S_IRWXG)
    Path(current_loc).rename(mv_loc)

    MZ_container.stop()
    time.sleep(2)
    MZ_container.remove()



def run_container(mzML_data_folder):
    global client,image,local_mem,command_list_2
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")
    save_mem = os.path.join(os.getcwd(),"IV_Features_csv")
    os.makedirs("./IV_Features_csv_tmp", exist_ok=True)
    os.makedirs("./IV_Features_csv", exist_ok=True)
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))


# TODO conditionally execute based on config?
    # Build a dict of all files in unprocessed-directory of
    #   KEY: <filename no suffix>
    #   VALUE: a tuple of (<filepath>, <filename suffix>)
    raw_files_no_ext_map = {Path(file).with_suffix('').name: (file, Path(file).suffix) for file in file_list}
    # Get list of already processed file
    file_list_processed = list(pathlib.Path("./IV_Features_csv").glob('*'))
    # Build a dict of all files in already-processed-directory of
    #   KEY: <filename without suffix>
    #   VALUE: a tuple of (filepath, suffix)
    processed_files_no_ext_map = {os.path.basename(os.path.splitext(os.path.splitext(Path(file).absolute())[0])[0]): (file, "".join(Path(file).suffixes)) for file in file_list_processed}
    # find the difference in processed and unprocessed sets built from the keys of both dicts
    unprocessed_names_map = list(set(raw_files_no_ext_map.keys()).difference(set(processed_files_no_ext_map.keys())))
    # transform difference list of kvps back into list of unprocessed filepaths of type pathlib.Path
    file_list = [raw_files_no_ext_map[key][0].with_suffix(raw_files_no_ext_map[key][1]) for key in unprocessed_names_map]
    print(f'found unprocessed files count: {len(file_list)}')
    

    process_num = len(file_list)
    if process_num > 4:
        process_num = 4

    if process_num == 0:
        return local_mem
    
    pool = Pool(processes=process_num)
    # pool.map(process, file_list)

    for _ in tqdm.tqdm(pool.imap(process, file_list), total=len(file_list), leave=None):
            pass

    pool.close()
    pool.join()
    return local_mem
