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

# sed -i 's/REPLACE_THIS_LINE/        <parameter name="Raw data file names"><file>\/Work\/III_mzML\/Dorrestein_GnPS_P14_G10_msms_POS_01Dec20_Fiji_Infusion_Min50_MA-csum-Min20_1.mzML<\/file><\/parameter>/' /Work/MZmine_FeatureFinder-batch.xml
# bash /MZmine-2.41.2/startMZmine_Linux.sh /Work/MZmine_FeatureFinder-batch.xml

#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

local_mem = os.path.join(os.getcwd(),"IV_Features_csv_tmp")
save_mem = os.path.join(os.getcwd(),"IV_Features_csv")

def process(filepath):
    global image,local_mem,command_list,save_mem
    file_path = str(filepath.absolute())
    file_name = os.path.basename(file_path)
    options = ["--bind", local_mem +":/tmp/IV_Features_csv"]
    # options = ["--bind", "/vagrant/dev_dockerized/drf/backend/mzMLData:/home/vagrant"]
    myinstance = Client.instance('./mzmine.sif', options=options)
    MZ_container = myinstance.name
    
    
    print("A")
    # Client.execute(myinstance,["mkdir","/home/vagrant/tmp"])
    # Client.execute(myinstance,["cp","/Work/MZmine_FeatureFinder-batch.xml", "/home/vagrant/MZmine_FeatureFinder-batch.xml"])
    print("filepath is ", filepath)
    
    # tmp ="7s/.*/" + """        <parameter name="Raw data file names"><file>\/Work\/III_mzML/""" + file_name + """<\/file><\/parameter>""" + "/"
    command_list_0 = """Rscript /tmp/R_PARSE_II.R"""
    command_list_1 = """sed -i 's/REPLACE_THIS_LINE/        <parameter name="Raw data file names"><file>\/Work\/III_mzML\/""" +file_name + """<\/file><\/parameter>/' /Work/MZmine_FeatureFinder-batch.xml"""
    print("B")
    Client.execute(myinstance,command_list_0)
    print("C")
    Client.execute(myinstance,command_list_1)
    
    # copy_dst = cont_name + ":/tmp/III_mzML/"
    shutil.copy(file_path, os.path.join(local_mem))

    print("D")
    Client.execute(myinstance,["bash","/MZmine-2.41.2/startMZmine_Linux.sh", "/Work/MZmine_FeatureFinder-batch.xml"])
    print("E")
    # # #Client.execute(myinstance,["mv","/Work/IV_Features_csv/*.csv", "/home/vagrant"])
    print("Instance complete: ",myinstance,"   ",filepath)
    current_loc = (os.path.join(local_mem,os.path.basename(file_path)))
    current_loc = current_loc + "_c_dc_de.csv"
    mv_loc = (os.path.join(save_mem,os.path.basename(file_path)))
    mv_loc = mv_loc + "_c_dc_de.csv"
    # os.chmod(current_loc,stat.S_IRWXG)
    Path(current_loc).rename(mv_loc)

    MZ_container.stop()
    time.sleep(2)

def run_container(mzML_data_folder):
    #main container
    global local_mem, save_mem
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
    print("unprocessed_names_map: ",unprocessed_names_map)
    print("raw_files_no_ext_map: ",raw_files_no_ext_map)
    
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

    print("\n_________________\MZmine Complete.\n_________________\n")
    # OUTPUT= tarfile.open("mzML_Zipfile","w")
    # OUTPUT.add('//vagrant/dev_dockerized/drf/backend/TEST_pipeline/mzML_Files')
    # OUTPUT.close()



# steps: 
# Main
# 1) Open minio client. Copy PP data to location, untar it.
# 2) For each file in PP, run a container.
# Ind Container steps:
# 3) mount container
# 4) copy file to container. (or maybe not because it is mounted)
# 5) run proteowizard
# 6) close container
#  Main
# 7) return data to minio





#Copy Functions: Copy from local Path to Path destination in a container.
#These require files to be in .tar format (so these are converted here, then transfered).

#Copy File functions
# def copy_a_file(client, src,dst):
#     name, dst = dst.split(':')
#     container = client.containers.get(name)
#     os.chdir(os.path.dirname(src))
#     srcname = os.path.basename(src) 
#     tar = tarfile.open(src + '.tar', mode='w')
#     try:
#         tar.add(srcname)
#     finally:
#         tar.close()
#     data = open(src + '.tar', 'rb').read()
#     container.put_archive(os.path.dirname(dst), data)
#     os.remove((src + '.tar'))

# def copy_some_files(client, src_list,dst):
#     for src in src_list:
#         srcname = os.path.basename(src)
#         dst = dst + srcname
#         copy_a_file(client, src,dst)



# def process(filepath):
#     global client,image,local_mem,command_list
#     file_path = str(filepath.absolute())
#     cont_name = ("PW_container_" + os.path.basename(file_path))
#     client.containers.run(image,name=cont_name,volumes={local_mem: {'bind': '/III_mzML', 'mode': 'rw'}}, detach=True, tty=True)
#     print("Container started: ", cont_name)
#     PW_container = client.containers.get(cont_name)
#     copy_dst = cont_name + ":/III_mzML/"
#     copy_a_file(client, file_path,copy_dst)
#     print("Files copied to container: ", cont_name)
#     command_list.pop()
#     command_list.append(("/III_mzML/" + os.path.basename(file_path)))
#     print("Proteowizard msconvert started in container: ",cont_name)
#     PW_container.exec_run(cmd=command_list)
#     print("Proteowizard completed in container: ", cont_name)
    
#     PW_container.stop()
#     time.sleep(2)
#     PW_container.remove()

# def run_container(raw_file_folder,exptype):
#     global client,image,local_mem,command_list
#     cur_dir = os.path.dirname(__file__)
#     os.chdir(cur_dir)
#     local_mem = os.getcwd() + "/III_mzML"
#     print("ProteoWizard Working Directory: ", local_mem)
#     # print("directory is:", os.getcwd())
#     # print("local mem is: ", local_mem)
#     os.makedirs("./III_mzML", exist_ok = True)

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))
    # print("TYPE:  ", type(file_list))

    #test for mac

    # file_list = list(pathlib.Path(raw_file_folder).glob('*'))

    # # if singlefield...
    # # if exptype == "Single":

    # #If Single field data is not Singlefield (determined by suffix), this will do something.
    # if exptype == "Single":
    #     print('Note: Running Single-Field Workflow, any files that do not contain ms1 data will be removed.')
    #     filtered_files =[]
    #     for item in file_list:
    #         ms_level = "no_suffix"
    #         raw_item = "{}".format(item)
    #         try:
    #             print("raw_item is:", raw_item)
    #             ms_level = re.search(r'\_([0-9]+)\.d', raw_item).group(1)
    #             print("ms level of ", raw_item, " is ", ms_level)
    #         except:
    #             pass
    #         if ms_level == "1" or ms_level == "no_suffix":
    #             filtered_files.append(item)
    #         else:
    #             print("File not included due to ms level indicated by naming suffix (..._2-#).d,: ", item)
    #     file_list = filtered_files

    # #This limits containers to 10 at a time. This is important for running locally.
    # #If this ever hits the cloud, "the limit does not exist!"
    # #This generates subprocesses - each subprocess runs a container which runs one file.
    # process_num = len(file_list)
    # if process_num > 10:
    #     process_num = 10

    # pool = Pool(processes=process_num)
    # pool.map(process, file_list)

    # pool.close()
    # pool.join()
    # return local_mem
