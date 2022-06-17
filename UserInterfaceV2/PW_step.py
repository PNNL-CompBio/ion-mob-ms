#!/usr/bin/env python3.9

import sys
import docker
import os
import tarfile
import time
import platform
import pathlib
import threading

#Copy file functions
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

def process(filepath,client,image,local_mem,command_list):
    file_path = str(filepath.absolute())
    cont_name = ("PW_container" + os.path.basename(file_path))
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, detach=True, tty=True)
    PW_container = client.containers.get(cont_name)
    copy_dst = cont_name + ":/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    command_list.pop()
    command_list.append(("/III_mzML/" + os.path.basename(file_path)))
    PW_container.exec_run(cmd=command_list)
    PW_container.stop()
    PW_container.remove()


def run_container(raw_file_folder):

    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    image = "anubhav0fnu/proteowizard"    
    local_mem = os.getcwd() + "/III_mzML"
    print("locsl mem: ",local_mem)
    client = docker.from_env()
    command_list = ["wine", "msconvert", "--zlib", "-e",".mzML.gz","-o","/III_mzML", "placeholder"]

    threads = [] 
    count = 0

    for filepath in pathlib.Path(raw_file_folder).glob('*'):
        threads.append(threading.Thread(target=process(filepath,client,image,local_mem,command_list)))  
        threads[count].start()
        count +=1
    for t in threads:
        t.join()
    return local_mem

