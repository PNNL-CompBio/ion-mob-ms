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

#Set initial variables,
#Determine local mem
client = docker.from_env()
image = "anubhav0fnu/proteowizard"    
local_mem = os.getcwd() + "/III_mzML_tmp"
save_mem = os.getcwd() + "/III_mzML"
# command_list = ["wine", "msconvert", "--zlib", "-e",".mzML.gz","-o","/III_mzML", "placeholder"]

#This is the command that will be run in the container
#Wine is used because Proteowizard/msconvert is a windows tool.
command_list = ["wine", "msconvert", "-e",".mzML","-o","/III_mzML", "placeholder"]


#Copy Functions: Copy from local Path to Path destination in a container.
#These require files to be in .tar format (so these are converted here, then transfered).

#Copy File functions
def copy_a_file(client, src,dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src) 
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
        print(os.path.dirname(src)," debug_line 1")
        time.sleep(1)
    finally:
        tar.close()
        print(os.path.dirname(src)," debug_line 2")
    time.sleep(1)
    data = open(src + '.tar', 'rb').read()
    time.sleep(1)
    print(os.path.dirname(src), " debug_line 3")
    container.put_archive(os.path.dirname(dst), data)
    print(os.path.dirname(src), " debug_line 4")
    time.sleep(1)
    os.remove((src + '.tar'))
    print(os.path.dirname(src), " debug_line 5")

def copy_some_files(client, src_list,dst):
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src,dst)


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
    copy_dst = cont_name + ":/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    print("Files copied to container: ", cont_name)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    print("Proteowizard msconvert started in container: ",cont_name)
    time.sleep(1)
    PW_container.exec_run(cmd=command_list)
    print("Proteowizard completed in container: ", cont_name)
    time.sleep(1)
    ##
    current_loc = (local_mem +"\\" + os.path.basename(file_path))
    shutil.rmtree(current_loc, onerror=onerror)
    # shutil.rmtree(current_loc)
    #remove .d, add .mzml
    print(os.path.basename(file_path), ": shutil")
    current_loc = current_loc[:-2] + ".mzML"
    mv_loc = (save_mem +"\\" + os.path.basename(file_path))
    mv_loc = mv_loc[:-2] + ".mzML"
    Path(current_loc).rename(mv_loc)
    print(os.path.basename(file_path), ": rename")
    ##
    time.sleep(1)
    PW_container.stop()
    time.sleep(2)
    PW_container.remove()
    time.sleep(1)
    
    
    

def run_container(raw_file_folder,exptype):
    global client,image,local_mem,command_list,save_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.getcwd() + "/III_mzML_tmp"
    save_mem = os.getcwd() + "/III_mzML"
    print("ProteoWizard Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./III_mzML", exist_ok = True)
    os.makedirs("./III_mzML_tmp", exist_ok = True)

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))

    #test for mac

    file_list = list(pathlib.Path(raw_file_folder).glob('*'))

    # if singlefield...
    # if exptype == "Single":

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

    #This limits containers to 10 at a time. This is important for running locally.
    #If this ever hits the cloud, "the limit does not exist!"
    #This generates subprocesses - each subprocess runs a container which runs one file.
    process_num = len(file_list)
    if process_num > 1:
        process_num = 1

    pool = Pool(processes=process_num)
    pool.map(process, file_list)

    pool.close()
    pool.join()
    shutil.rmtree(local_mem)
    return save_mem

