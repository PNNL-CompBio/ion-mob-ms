#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import sys
import docker
import os
import tarfile
import time
import platform

#This step defines the run method of autoCCS.
#Code could certainly be improved.
#Tip for improving: look at other step.py files.
#could share a copy function that works for both mac and windows


command_0 = """Rscript /R_Metadata_I.R"""
command_tmp_fix_for_0 = """python3.8 /fix_metadata.py"""
command_annotate = """Rscript /R_Annotate_features_V.R"""

#Copy Functions: Copy from local Path to Path destination in a container.
#These require files to be in .tar format (so these are converted here, then transfered).

#Mac copy file functions
def copy_a_file_mac(client, src,dst):
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

def copy_some_files_mac(client, src_list,dst):
    for src in src_list:
        srcname = os.path.basename(src)
        dst = dst + srcname
        copy_a_file_mac(client, src,dst)

#PC copy file functions
#These files are received slightly different from mac, so they just require updated string formating.
#However, if you look at other step.py files, these functions could be converged.
def copy_a_file_PC(client, src,dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)
    srcname = os.path.basename(src).replace('"',"")
    src = src.replace('"',"")
    os.chdir(os.path.dirname(src))
    tar = tarfile.open(src + '.tar', mode='w')
    tar.add(srcname)
    tar.close()
    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
    os.remove((src + '.tar'))

def copy_some_files_PC(client, src_list,dst):
    for src in src_list:
        if src != "":
            srcname = os.path.basename(src)
            dst = dst + srcname
            copy_a_file_PC(client, src,dst)



def run_container(exp,version,annotate,calibrant_file,framemeta_files, feature_files, target_list_file,raw_file_metadata,preP_files):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)


    #Reformat path strings depending on mac or windows.
    if platform.system().upper() == "DARWIN":
        feature_files=feature_files.replace(" ", "\ ")
        cmd2 = "echo " + feature_files
        F_files = os.popen(cmd2).read()
        F_files = F_files.strip()
        F_files = F_files.split(" /")
        counter = 1
        for item in F_files[1:]:
            F_files[counter] =  "/" + item
            counter +=1
        local_mem = os.getcwd() + "/IV_data"

    if platform.system().upper() == "WINDOWS":
        feature_files_quote = '"' + feature_files + '"'
        cmd2 = "dir/b " + feature_files_quote
        F_files = os.popen(cmd2).read()
        F_files = F_files.split("\n")
        counter = 0
        for item in F_files[:-1]:
            F_files[counter] = '"'+ feature_files[:-5] + item +'"'
            counter +=1
        local_mem = os.getcwd() + "\\IV_data"

    if exp == "single":
        if platform.system().upper() == "WINDOWS": 
            PP_files_quote = '"' + preP_files + '"'
            cmd3 = "dir/b " + PP_files_quote
            PP_files = os.popen(cmd3).read()
            PP_files = PP_files.split("\n")
            counter = 0
            for item in PP_files[:-1]:
                PP_files[counter] = '"'+ preP_files + "/"+ item +'"'
                counter +=1
        if platform.system().upper() == "DARWIN":
            PP_files=preP_files.replace(" ", "\ ")
            cmd2 = "echo " + PP_files
            PP_files = os.popen(cmd2).read()
            PP_files = PP_files.strip()
            PP_files = PP_files.split(" /")
            counter = 1
            for item in PP_files[1:]:
                PP_files[counter] =  "/" + item
                counter +=1
            local_mem = os.getcwd() + "/IV_data"


#Determine which command line options will be used.
#This was kept in this longer format because it is easier to modify. 
#Note: If modifying these... any that use a wildcard, MUST use single quotes
#such as ('/tmp/FF/*.csv'). If you use double quotes, this will fail. Why? who knows...
    if version == "standard":
        if exp == "single":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_single_config.xml", "--feature_files", '/tmp/FF/*.csv', 
            "--sample_meta", "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--output_dir", "/tmp/IV_Results", "--mode", "single",
            "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "AgTune", "--colname_for_sample_type", "SampleType", "--single_mode", "batch"]
            # command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_single_config.xml", "--feature_files", '/tmp/FF/*.csv', 
            # "--sample_meta", ("/tmp/MD/" + os.path.basename(raw_file_metadata)), "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--output_dir", "/tmp/IV_Results", "--mode", "single",
            # "--colname_for_filename", "RawFileName", "--single_mode", "batch"]

        elif exp == "slim":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_slim_config.xml", "--feature_files", '/tmp/FF/*.csv', 
            "--output_dir", "/tmp/IV_Results", "--sample_meta", ("/tmp/MD/" + os.path.basename(raw_file_metadata)),"--mode", "single", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)),
            "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "Calibrant", "--colname_for_sample_type", "SampleType", "--colname_for_ionization", "IonPolarity", "--single_mode", "batch", "--degree", "2", "--calib_method", "power"]
    
    if version == "enhanced": 
        if exp == "single":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_single_config.xml", "--framemeta_files", '/tmp/FMF/*.txt', "--sample_meta", 
            "/tmp/MD/RawFiles_Metadata.csv", "--calibrant_file", ("/tmp/CBF/" + os.path.basename(calibrant_file)), "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--mode", 
            "single", "--colname_for_filename", "RawFileName", "--tunemix_sample_type", "AgTune", "--colname_for_sample_type", "SampleType", "--single_mode", "batch"]
        elif exp == "step":
            command_list = ["python3.8","/AutoCCS/autoCCS.py", "--config_file", "/tmp/CF/autoCCS_step_config.xml", "--framemeta_files",
            '/tmp/FMF/*.txt', "--feature_files", '/tmp/FF/*.csv', "--output_dir", "/tmp/IV_Results", "--target_list_file", ("/tmp/TLF/" + os.path.basename(target_list_file)), "--mode", "multi"]
       

       #Reformat string paths depending on mac or windows
        if platform.system().upper() == "DARWIN":
            framemeta_files=framemeta_files.replace(" ", "\ ")
            cmd1 = "echo " + framemeta_files
            new_framefiles = os.popen(cmd1).read()
            new_framefiles = new_framefiles.strip()
            new_framefiles = new_framefiles.split(" /")
            counter = 1
            for item in new_framefiles[1:]:
                new_framefiles[counter] =  "/" + item
                counter +=1
        if platform.system().upper() == "WINDOWS": 
            framemeta_files_quote = '"' + framemeta_files + '"'
            cmd1 = "dir/b " + framemeta_files_quote
            new_framefiles = os.popen(cmd1).read()
            new_framefiles = new_framefiles.split("\n")
            counter = 0
            for item in new_framefiles[:-1]:
                new_framefiles[counter] = '"'+ framemeta_files[:-5] + item +'"'
                counter +=1

    #This prints where the local files are being saved to. (With pyinstaller, this is a temporary folder)
    print("Local memory is: ", local_mem)
    #Image name
    image = "anubhav0fnu/autoccs"    
    #Make file system
    os.makedirs("./IV_data/PP", exist_ok=True)
    os.makedirs("./IV_data/CF", exist_ok=True)
    os.makedirs("./IV_data/TLF", exist_ok=True)
    os.makedirs("./IV_data/FF", exist_ok=True)
    os.makedirs("./IV_data/IV_Results", exist_ok=True)
    os.makedirs("./IV_data/FMF", exist_ok=True)
    os.makedirs("./IV_data/MD", exist_ok=True)
    os.makedirs("./IV_data/CBF", exist_ok=True)
    time.sleep(5)
    print("Z\n")

    #choose which config file will be used
    command_single = ["mv", "/tmp_autoccs/autoCCS_single_config.xml", "/tmp/CF"]
    command_step = ["mv", "/tmp_autoccs/autoCCS_step_config.xml", "/tmp/CF"]
    command_slim = ["mv", "/tmp_autoccs/autoCCS_slim_config.xml", "/tmp/CF"]

    #start container
    #mount local mem (path/IV_data) to /tmp in the container
    #in the container, all the subdirectories above are in /tmp path
    #Container is interactive. You can open a terminal (recc: then use bash) and see data & manually run autoCCS.
    client = docker.from_env()
    print("Y\n")
    client.containers.run(image,name="AC_container",volumes={local_mem: {'bind': '/tmp', 'mode': 'rw'}}, detach=True, tty=True)
    AC_Container = client.containers.get('AC_container')
    print("A\n")
    if platform.system().upper() == "DARWIN":
        if exp == "single":
            AC_Container.exec_run(cmd=command_single)
            copy_some_files_mac(client, PP_files, 'AC_container:/tmp/PP/files')
            copy_a_file_mac(client, calibrant_file, 'AC_container:/tmp/CBF/calibrant_file')
            print("B\n")
        if exp == "slim":
            AC_Container.exec_run(cmd=command_slim)
            copy_a_file_mac(client, raw_file_metadata, 'AC_container:/tmp/MD/meta_data')
            copy_a_file_mac(client, calibrant_file, 'AC_container:/tmp/CBF/calibrant_file')
            print("B\n")
        if version == "enhanced":
            copy_some_files_mac(client, new_framefiles, 'AC_container:/tmp/FMF/framemeta_files')
        print("C\n")
        copy_some_files_mac(client, F_files, 'AC_container:/tmp/FF/feature_files')
        print("D\n")
        if exp == "step":
            AC_Container.exec_run(cmd=command_step)
            copy_a_file_mac(client, target_list_file, 'AC_container:/tmp/TLF/target_list_file')
        time.sleep(5)
        print("F\n")
        if annotate == True:
            copy_a_file_mac(client,target_list_file, 'AC_container:/tmp/TLF/target_list_file')

        #single field performs automated metadata extraction.
        #If this is ever not working, code can be modified to include this. See Notes in UI_V2.py.
        #slim requires user-generated metadata
        #stepped field determines metadata from filename.
        if exp == "single":
            AC_Container.exec_run(cmd=command_0)
            print("Metadata extracted")
            AC_Container.exec_run(cmd=command_tmp_fix_for_0)
            print("Metadata Fixed")
        time.sleep(3)
        #run autoCCS
        AC_Container.exec_run(cmd=command_list)
        time.sleep(3)
        print("G\n")
        if annotate == True:
            AC_Container.exec_run(cmd=command_annotate)
            print("Annotations complete")
            time.sleep(3)
        #You can comment out .stop and .remove to use interactive mode with the AC_Container.
        AC_Container.stop()
        print("H\n")
        AC_Container.remove()
        print("I\n")
        return local_mem
        
    if platform.system().upper() == "WINDOWS":
        print("AC container running on PC")
        if exp == "single":
            AC_Container.exec_run(cmd=command_single)
            copy_some_files_PC(client, PP_files, 'AC_container:/tmp/PP/files')
            copy_a_file_PC(client, calibrant_file, 'AC_container:/tmp/CBF/calibrant_file')
            print("B\n")
        if exp == "slim":
            AC_Container.exec_run(cmd=command_slim)
            copy_a_file_PC(client, raw_file_metadata, 'AC_container:/tmp/MD/meta_data')
            copy_a_file_PC(client, calibrant_file, 'AC_container:/tmp/CBF/calibrant_file')
            print("B\n")
        if version == "enhanced":
            copy_some_files_PC(client, new_framefiles, 'AC_container:/tmp/FMF/framemeta_files')
        print("C\n")
        copy_some_files_PC(client, F_files, 'AC_container:/tmp/FF/feature_files')
        print("D\n")
        if exp == "step":
            AC_Container.exec_run(cmd=command_step)
            copy_a_file_PC(client, target_list_file, 'AC_container:/tmp/TLF/target_list_file')
        if annotate == True:
            copy_a_file_PC(client,target_list_file, 'AC_container:/tmp/TLF/target_list_file')


        if exp == "single":
            AC_Container.exec_run(cmd=command_0)
            print("Metadata extracted")
            AC_Container.exec_run(cmd=command_tmp_fix_for_0)
            print("Metadata Fixed")
        time.sleep(3)
        print("F\n")
        AC_Container.exec_run(cmd=command_list)
        time.sleep(3)
        print("G\n")
        print("THE value of annotate is: ", annotate)
        print("The value of command_annotate is: ", command_annotate)
        if annotate == True:
            AC_Container.exec_run(cmd=command_annotate)
            print("Annotations complete")
            time.sleep(3)
        AC_Container.stop()
        # print("H\n")
        AC_Container.remove()
        print("I\n")
        return local_mem


