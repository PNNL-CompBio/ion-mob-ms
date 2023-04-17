#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import argparse
import json
import subprocess
import sys
# import docker
import os
import tarfile
import time
import platform
import PW_hpc
import MZ_hpc
# import PP_step
# import DM_step
import AC_hpc
from datetime import datetime

#add timestamps to print
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

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
        print("Json file passed to Pipeline.py")
        print("Single Field Begins here.")
        # if "PP" in data[0]["ToolType"]:
        #     print("PNNL Preprocessor does Filtering and Smoothing")
        #     PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_hpc.run_container("single","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
        
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" in data[1]:
            AC_results= AC_hpc.run_container("single","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
            print("AutoCCS finds features through the standard method. \nTarget list specified, annotations will proceed after AutoCCS.")

        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the enhanced method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_hpc.run_container("single","enhanced",False, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
    
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" in data[1]:
            print("AutoCCS finds features through the enhanced method. \nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_hpc.run_container("single","enhanced",True, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"],data[1]["Target List File"], False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])


    ## Slim 
    if data[0]["ExpType"] == "SLIM":
        print("Json file passed to Pipeline.py")
        print("SLIM Begins here.")
        # if data[1]["Experiment"]
        # if "PP" in data[0]["ToolType"]:
        #     print("PNNL Preprocessor does Filtering and Smoothing")
        #     PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method.\nNo Target list specified, annotations will be skipped. ")
            AC_results= AC_hpc.run_container("slim","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
        if "AC" in data[0]["ToolType"] and "Target List File" in data[1]:
            print("AutoCCS finds features through the standard method.\nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_hpc.run_container("slim","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
        

    ## Stepped Field
    if data[0]["ExpType"] == "Stepped":
        print("Json file passed to Pipeline.py")
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
        # if "PP" in data[0]["ToolType"]:
        #     print("PNNL Preprocessor does Filtering and Smoothing")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_hpc.run_container("step","enhanced",True,False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False,False,data[1]["AutoCCS Config File"])
    

    #This required for the GUI to identify which tools were completed.
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results
