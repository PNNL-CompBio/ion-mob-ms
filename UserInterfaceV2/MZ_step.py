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
image = "anubhav0fnu/mzmine:latest"
local_mem = os.getcwd() + "/IV_Features_csv"
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


# def edit_xml_file(file_name):
#     with open("/tmp/MZmine_FeatureFinder-batch.xml","w") as file:
#         counter = 1
#         for line in file:
#             if counter == 7:
#                 edited_line = '        <parameter name="Raw data file names"><file>/tmp/III_mzML/' + file_name + "</file></parameter>"
#                 file.write(edited_line)
#             else:
#                 file.write(line)
#             counter +=1





def process(filepath):
    global client,image,local_mem,command_list_2
    time.sleep(2)
    file_path = str(filepath.absolute())
    cont_name = ("MZ_container_" + os.path.basename(file_path))
    file_name = os.path.basename(file_path)
    client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/tmp/IV_Features_csv', 'mode': 'rw'}}, detach=True, tty=True)
    print("Container started: ", cont_name)
    MZ_container = client.containers.get(cont_name)
    # edited_line = '        <parameter name="Raw data file names"><file>/tmp/III_mzML/' + file_name + "</file></parameter>"
    # line_replace = "'s/REPLACE_THIS_LINE/" + edited_line + "/'"
    # command_list_1 = ["sed", "-i", line_replace, "/tmp/MZmine_FeatureFinder-batch.xml"]
    command_list_1 = """sed -i 's/REPLACE_THIS_LINE/        <parameter name="Raw data file names"><file>\/tmp\/III_mzML\/""" +file_name + """<\/file><\/parameter>/' /tmp/MZmine_FeatureFinder-batch.xml"""
    print("command_list_one:   ", command_list_1 )
    copy_dst = cont_name + ":/tmp/III_mzML/"
    copy_a_file(client, file_path,copy_dst)
    command_list_0 = """Rscript /tmp/R_PARSE_II.R"""
    print("Files copied to container: ", cont_name)
    print("MzMine started in container: ",cont_name)
    MZ_container.exec_run(cmd=command_list_0)
    MZ_container.exec_run(cmd=command_list_1)
    MZ_container.exec_run(cmd=command_list_2)
    print("MzMine completed in container: ", cont_name)
    MZ_container.stop()
    MZ_container.remove()

def run_container(mzML_data_folder):
    global client,image,local_mem,command_list_2
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)

    local_mem = os.getcwd() + "/IV_Features_csv"
    print("MzMine Working Directory: ", local_mem)
    # print("directory is:", os.getcwd())
    # print("local mem is: ", local_mem)
    os.makedirs("./IV_Features_csv", exist_ok=True)
    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))
    print("mzml data folder varible: ",mzML_data_folder)
    file_list = list(pathlib.Path(mzML_data_folder).glob('*.mzML'))
    print("TYPE:  ", type(file_list))
    print("file list: ",file_list)

    #process_num = len(file_list)
    process_num = len(file_list)
    if process_num > 10:
        process_num = 10
        
    pool = Pool(processes=process_num)
    pool.map(process, file_list)

    pool.close()
    pool.join()
    return local_mem