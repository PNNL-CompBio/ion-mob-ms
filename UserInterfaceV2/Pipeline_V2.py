#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

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

#This manages the individual steps.
#It receives a json file, which includes the desired tools, and experiment type.
#It runs through each step until completion or failure.

def execute_workflow(json_file):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    f = open(json_file)
    data = json.load(f)
    f.close()

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
            PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
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
            AC_results= AC_step.run_container("single","standard", data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("single","enhanced", data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,data[1]["PreProcessed Data Folder"])

    ## Slim 
    if data[0]["ExpType"] == "SLIM":
        print("SLIM Begins here.")
        # if data[1]["Experiment"]
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
            PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        if "DM" in data[0]["ToolType"]:
            print("Deimos searches for Features")
            DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1]:
            print("AutoCCS finds features through the standard method.")
            AC_results= AC_step.run_container("slim","standard", data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False)
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_step.run_container("slim","enhanced", data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False)

    ## Stepped Field
    if data[0]["ExpType"] == "Stepped":
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
        if "PP" in data[0]["ToolType"]:
            print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
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
            AC_results= AC_step.run_container("step","enhanced",False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False,False)
    

    #This required for the GUI to identify which tools were completed.
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results