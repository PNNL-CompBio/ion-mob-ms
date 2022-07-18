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
image = "jjacobson95/pnnl_preprocessor4"    
local_mem = os.getcwd() + "/II_Preprocessed"
command_0 = """Rscript /tmp/R_Metadata_I.R"""
#command_list_1 = ["wine", "PNNL-PreProcessor.exe", "-smooth","-driftKernel","placeholder_1","-lcKernel","placeholder_2","-minIntensity","placeholder_3","-split,I_Raw,II_Preprocessed"]
command_list_1 = ["C:\\PNNL-Preprocessor_4.0_2022.02.17\\PNNL-Preprocessor\\PNNL-PreProcessor.exe", "-smooth","-driftKernel","1","-lcKernel","0","-minIntensity","20","-split","-r","-d",'"..\\..\\tmp\\II_Preprocessed\\I_Raw"']

# PNNL-PreProcessor.exe -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split -r -d "..\\..\\tmp\\I_Raw"
# PNNL-PreProcessor.exe -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split -r -d "..\\..\\tmp\\II_Preprocessed\\I_Raw"
# wine PNNL-PreProcessor.exe -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split -r -d "./tmp/I_Raw/"


#Copy file functions
#if mac
def copy_a_file(client, src,dst):
    if platform.system().upper() == "DARWIN":
        name, dst = dst.split(':')
    if platform.system().upper() == "WINDOWS":
        name = dst[:-6]
        dst = dst[-6:]
        print("name: ", name)
        print("dst: ", dst)
    container = client.containers.get(name)
    print("A")
    os.chdir(os.path.dirname(src))
    print("B")
    srcname = os.path.basename(src) 
    print("C")
    tar = tarfile.open(src + '.tar', mode='w')
    print("D")
    try:
        tar.add(srcname)
    finally:
        tar.close()
    print("E")
    data = open(src + '.tar', 'rb').read()
    print("F")
    container.put_archive(os.path.dirname(dst), data)
    print("G")
    os.remove((src + '.tar'))

def copy_some_files(client, src_list,dst):
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file(client, src,dst)



# os.makedirs("./III_mzML", exist_ok=True)


def copy_files_V2_windows(src,loc):
    cmd = "Xcopy " + '"' + src + '"'+ " " + '"' + loc + "/I_Raw" + '"' + " /E /H /I"
    print("command is ", cmd)
    os.system(cmd)
    #cont.exec_run(cmd=command_0)



def process(filepath,drift_val,lc_val,minI_val):
    global client,image,local_mem,command_list
    file_path = filepath
    cont_name = ("PP_container")
    command_list_1[3] = drift_val
    command_list_1[5] = lc_val
    command_list_1[7] = minI_val
    copy_files_V2_windows(file_path, local_mem)
    listy = ["mkdir .\\XXX"]
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/II_Preprocessed', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    PP_container = client.containers.get(cont_name)
    if platform.system().upper() == "DARWIN":
        print("Darwin")
        copy_dst = cont_name + ":/tmp/"
    if platform.system().upper() == "WINDOWS":
        print("Windows")
        copy_dst = cont_name + "C:\\tmp"
        # copy_files_V2_windows(file_path, PP_container, local_mem)
    # copy_a_file(client, file_path,copy_dst)
    # copy_some_files(client, file_path, 'PP_container:/tmp')
    print("Files copied to container: ", cont_name)
    # command_list_1[3] = drift_val
    # command_list_1[5] = lc_val
    # command_list_1[7] = minI_val
    print("PNNL PreProcessor started in container: ",cont_name)
    #PP_container.exec_run(cmd=command_0)
    print("Metadata Extracted. ")
    # for item in command_list_1:
    #     print("cmd list 1 item ", item)
    listy = ["mkdir .\\XXX"]
    PP_container.exec_run(cmd="mkdir test_dir")
    # PP_container.exec_run(cmd=command_list_1)
    print("PNNL PreProcessor completed in container: ", cont_name)
    
    # PP_container.stop()
    # PP_container.remove()

def run_container(raw_file_folder,drift_val,lc_val,minI_val):
    global client,image,local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    print("curdur is: ",cur_dir)
    local_mem = os.getcwd() + "/II_Preprocessed"
    print("PNNL PreProcessor Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./II_Preprocessed", exist_ok = True)

    process(raw_file_folder,drift_val,lc_val,minI_val)

    return local_mem

