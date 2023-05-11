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



#This is Deimos!
#More optimization is required here. Deimos should run much faster, but 
#due to some issue with container resources, it runs quite slow at this time.


client = docker.from_env()
image = "anubhav0fnu/ccs_comparison"
local_mem = os.getcwd() + "/IV_Features_csv"
#command_list_2 = ["bash", "startMZmine_Linux.sh", "/tmp/MZmine_FeatureFinder-batch.xml"]


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
    global client,image,local_mem
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("DM_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    #If memory issues are occuring, increase the maximum here (mem_limit). This should be enough for any files.
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/IV_Features_csv', 'mode': 'rw'}}, mem_limit="14g",detach=True, tty=True)
    print("Container started: ", cont_name)
    DM_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/III_mzML/"
    #copy_dst = cont_name + ":/tmp/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    print("Files copied to container: ", cont_name)
    print("Deimos started in container: ",cont_name)
    DM_container.exec_run(cmd="python /tmp/deimos_feature_finder.py")
    print("Deimos completed in container: ", cont_name)
    time.sleep(1)
    DM_container.stop()
    time.sleep(2)
    DM_container.remove()

def run_container(mzML_data_folder):
    global client,image,local_mem
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    local_mem = os.getcwd() + "/IV_Features_csv"
    print("Deimos Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./IV_Features_csv", exist_ok=True)
    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))

    #process_num = len(file_list)
    
    #At this time, 3 in parallel seems to finish correctly and be the fastest option. (still slow)
    #If more processes are added, issues occur more regularly.
    process_num = len(file_list)
    if process_num > 3:
        process_num = 3
        
    pool = Pool(processes=process_num)
    pool.map(process, file_list)

    pool.close()
    pool.join()
    return local_mem