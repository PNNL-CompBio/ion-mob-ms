#!/usr/bin/env python3.9

import argparse
import json
import subprocess
import AC_step_PC
import sys
import docker
import os
import tarfile
import time


def execute_workflow(json_file):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    f = open(json_file)
    data = json.load(f)
    f.close()

    ## Single Field
    if data[0]["Experiment"] == 0:
        print("Single Field Begins here.")
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
        if data[1]["ds_1"] == True:
            print("Deimos searches for Features")
        if data[1]["ds_2"] == True:
            print("Deimos finds CCS values")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the standard method.")
            AC_step_PC.run_container("single","standard",data[3]["Calibrant Data"],False, data[3]["Feature Data"], False, data[3]["Raw File Metadata"])
        if data[1]["ac_2"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_step_PC.run_container("single","enhanced",data[3]["Calibrant Data"],data[3]["FrameMetadata"], data[3]["Feature Data"], False, data[3]["Raw File Metadata"])



    ## Slim 
    elif data[0]["Experiment"] == 1:
        print("SLIM Begins here.")
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
        if data[1]["ds_1"] == True:
            print("Deimos searches for Features")
        if data[1]["ds_2"] == True:
            print("Deimos finds CCS values")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the standard method.")
            AC_step_PC.run_container("single","standard",data[3]["Calibrant Data"],False, data[3]["Feature Data"], False, data[3]["Raw File Metadata"])
        if data[1]["ac_2"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_step_PC.run_container("single","enhanced",data[3]["Calibrant Data"], data[3]["FrameMetadata"], data[3]["Feature Data"], False, data[3]["Raw File Metadata"])
        

    #Stepped Field
    elif data[0]["Experiment"] == 2:
        print("Stepped Field Begins here.")
        if data[1]["pp_1"] == True:
            print("PNNL Preprocessor does Filtering")
        if data[1]["pp_2"] == True:
            print("PNNL Preprocessor does Smoothing")
        if data[1]["pw_1"] == True:
            print("Proteowizard converts Files")
        if data[1]["mm_1"] == True:
            print("MZMine searches for Features")
        if data[1]["ac_1"] == True:
            print("AutoCCS finds features through the enhanced method.")
            AC_step_PC.run_container("step","enhanced",False, data[3]["FrameMetadata"], data[3]["Feature Data"], data[3]["Target List"],False)

