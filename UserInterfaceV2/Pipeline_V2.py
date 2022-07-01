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
    if data[0]["ExpType"] == "Single" or data[0]["ExpType"] == "Any":
        print("Single Field Begins here.")
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["Raw Data Folder"])
        if "DM_1" in data[0]["ToolType"]:
            print("Deimos searches for Features")
        if "DM_2" in data[0]["ToolType"]:
            print("Deimos finds CCS values")
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1]:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("single","standard", data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("single","enhanced", data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, data[1]["Metadata File"])

    ## Slim 
    if data[0]["ExpType"] == "SLIM":
        print("SLIM Begins here.")
        # if data[1]["Experiment"]
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["Raw Data Folder"])
        if data[0]["ToolType"] == "DM" and "....":
            print("Deimos searches for Features")
        if data[0]["ToolType"] == "DM" and "......":
            print("Deimos finds CCS values")
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1]:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("single","standard",data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("single","enhanced",data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, data[1]["Metadata File"])

    ## Stepped Field
    if data[0]["ExpType"] == "Stepped":
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["Raw Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
        if "AC" in data[0]["ToolType"]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("step","enhanced",False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"],False)
    
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results