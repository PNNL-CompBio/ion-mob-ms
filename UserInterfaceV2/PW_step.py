#!/usr/bin/env python3.9

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
image = "anubhav0fnu/proteowizard"    
local_mem = os.getcwd() + "/III_mzML"
# command_list = ["wine", "msconvert", "--zlib", "-e",".mzML.gz","-o","/III_mzML", "placeholder"]
command_list = ["wine", "msconvert", "-e",".mzML","-o","/III_mzML", "placeholder"]


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



# os.makedirs("./III_mzML", exist_ok=True)



def process(filepath):
    global client,image,local_mem,command_list
    file_path = str(filepath.absolute())
    cont_name = ("PW_container_" + os.path.basename(file_path))
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    PW_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    print("Files copied to container: ", cont_name)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    print("Proteowizard started in container: ",cont_name)
    PW_container.exec_run(cmd=command_list)
    print("Proteowizard completed in container: ", cont_name)
    
    PW_container.stop()
    PW_container.remove()

def run_container(raw_file_folder):
    global client,image,local_mem,command_list
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.getcwd() + "/III_mzML"
    print("ProteoWizard Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./III_mzML", exist_ok = True)

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))
    
    file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))
    # print("file list: ",file_list)

    process_num = len(file_list)
    pool = Pool(processes=process_num)
    pool.map(process, file_list)

    pool.close()
    pool.join()
    return local_mem

