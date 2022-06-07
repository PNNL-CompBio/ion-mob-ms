#!/usr/bin/env python3.9

import argparse
import json
import subprocess
import AC_step
import sys
import docker
import os
import tarfile
import time
import platform
import PW_step


def execute_workflow(json_file):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    f = open(json_file)
    data = json.load(f)
    f.close()

#Mac and Windows are seperated here to avoid building host OS variables into docker images.
#Instead, "mac" and "pc" arguments are passed into the run_container functions.
    PP_results = ""
    PW_results = ""
    MZ_results = ""
    DM_results = ""
    AC_results = ""
    ## Single Field
    if data[0]["Experiment"] == 0:
        print("Single Field Begins here.")
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[3]["Raw Data Folder"])
        if data[1]["ds_1"] == True:
            print("Deimos searches for Features")
        if data[1]["ds_2"] == True:
            print("Deimos finds CCS values")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("single","standard",data[3]["Calibrant File"],False, data[3]["Feature Data Folder"], False, data[3]["Metadata File"])
        if data[1]["ac_2"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("single","enhanced",data[3]["Calibrant File"],data[3]["Ims Metadata Folder"], data[3]["Feature Data Folder"], False, data[3]["Metadata File"])

    ## Slim 
    if data[0]["Experiment"] == 1:
        print("SLIM Begins here.")
        # if data[1]["Experiment"]
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[3]["Raw Data Folder"])
        if data[1]["ds_1"] == True:
            print("Deimos searches for Features")
        if data[1]["ds_2"] == True:
            print("Deimos finds CCS values")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("single","standard",data[3]["Calibrant File"],False, data[3]["Feature Data Folder"], False, data[3]["Metadata File"])
        if data[1]["ac_2"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("single","enhanced",data[3]["Calibrant File"], data[3]["Ims Metadata Folder"], data[3]["Feature Data Folder"], False, data[3]["Metadata File"])

    ## Stepped Field
    if data[0]["Experiment"] == 2:
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[3]["Raw Data Folder"])
        if data[1]["mm_1"] == True:
            print("MZMine searches for Features")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("step","enhanced",False, data[3]["Ims Metadata Folder"], data[3]["Feature Data Folder"], data[3]["Target List File"],False)
    
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results