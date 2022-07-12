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
image = "jjacobson95/pnnl_preprocessor"    
local_mem = os.getcwd() + "/II_Preprocessed"
command_0 = """Rscript /tmp/R_Metadata_I.R"""
command_list_1 = ["wine", "PNNL-PreProcessor.exe", "-smooth","-driftKernel","placeholder_1","-lcKernel","placeholder_2","-minIntensity","placeholder_3","-split,I_Raw,II_Preprocessed"]

# wine PNNL-PreProcessor.exe -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split -r -d "./tmp/I_Raw/"


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



def process(filepath,drift_val,lc_val,minI_val):
    global client,image,local_mem,command_list
    file_path = filepath
    cont_name = ("PP_container")
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/II_Preprocessed', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    PP_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/tmp/"
    copy_a_file(client, file_path,copy_dst)
    # copy_some_files(client, file_path, 'PP_container:/tmp')
    print("Files copied to container: ", cont_name)
    command_list_1[4] = drift_val
    command_list_1[6] = lc_val
    command_list_1[8] = minI_val
    print("PNNL PreProcessor started in container: ",cont_name)
    PP_container.exec_run(cmd=command_0)
    print("Metadata Extracted. ",)
    PP_container.exec_run(cmd=command_list_1)
    print("PNNL PreProcessor completed in container: ", cont_name)
    
    # PP_container.stop()
    # PP_container.remove()

def run_container(raw_file_folder,drift_val,lc_val,minI_val):
    global client,image,local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    local_mem = os.getcwd() + "/II_Preprocessed"
    print("PNNL PreProcessor Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./II_Preprocessed", exist_ok = True)

    process(raw_file_folder,drift_val,lc_val,minI_val)

    return local_mem

