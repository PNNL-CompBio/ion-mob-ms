#!/usr/bin/env python3.9

import argparse
import json
import subprocess
import sys
import docker
import os
import tarfile
import time
import platform
import PW_step
import MZ_step
import PP_step
import DM_step
import AC_step


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
            PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"])
        if "DM" in data[0]["ToolType"]:
            print("Deimos searches for Features")
            DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
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
            PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["Raw Data Folder"])
        if "DM" in data[0]["ToolType"]:
            print("Deimos searches for Features")
            DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1]:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("slim","standard", data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("slim","enhanced", data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, data[1]["Metadata File"])

    ## Stepped Field
    if data[0]["ExpType"] == "Stepped":
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["Raw Data Folder"])
        if "DM" in data[0]["ToolType"]:
            print("Deimos searches for Features")
            DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("step","enhanced",False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False)
    
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results