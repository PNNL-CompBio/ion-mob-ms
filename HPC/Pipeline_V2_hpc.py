#!/usr/bin/env python3.9

"""
Pipeline_V2_hpc.py - Workflow Orchestration for HPC Environments

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    High-performance computing variant of pipeline orchestration using Singularity
    containers. Coordinates multi-stage mass spectrometry data processing workflows
    on HPC infrastructure with standard job scheduler integration (SLURM, SGE, PBS).
    
    This module manages the execution sequence of tool-specific HPC modules
    (PW_hpc, MZ_hpc, AC_hpc) based on experiment type and JSON configuration.
    Handles container image discovery, parameter passing, and workflow completion
    tracking for high-throughput batch analysis on shared HPC resources.
    
    Key Features:
    - JSON-driven workflow configuration
    - Experiment-type aware tool execution routing
    - Singularity image discovery and execution
    - Container parameter propagation
    - Batch job integration for HPC schedulers
    - Step-by-step workflow logging
"""

import argparse
import json
import subprocess
import sys
import os
import tarfile
import time
import platform
import PW_hpc
import MZ_hpc
import AC_hpc
from datetime import datetime

# HPC container runtime logging with timestamps
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print

print("CPUs detected: ",os.cpu_count())

def execute_workflow(json_file):
    """
    Execute multi-stage Singularity container workflow based on JSON configuration.
    
    Reads JSON configuration specifying experiment type, enabled tools, and data
    paths. Routes execution through appropriate HPC tool modules (PW_hpc, MZ_hpc,
    AC_hpc) based on experiment type and tool list specified in configuration.
    
    Supports three experiment types:
    - "Single": Single Field Ion Mobility data processing
    - "SLIM": SLIM (Structures for Lossless Ion Mobility) data processing  
    - "Stepped": Stepped Field Ion Mobility data processing
    
    Parameters:
        json_file (str): Path to JSON configuration file specifying workflow
                        including experiment type, tool types, and data paths
        
    Returns:
        dict: Dictionary containing results from each executed tool stage
    """
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    f = open(json_file)
    data = json.load(f)
    f.close()

    # Initialize results tracking for each tool stage
    PP_results = ""
    PW_results = ""
    MZ_results = ""
    DM_results = ""
    AC_results = ""


    # Single Field ion mobility workflow execution
    if data[0]["ExpType"] == "Single" or data[0]["ExpType"] == "Any":
        print("Json file passed to Pipeline.py")
        print("Single Field workflow begins execution.")
        # Execute Proteowizard data conversion if specified
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard: Converting raw data to mzML format")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[1]["mzML Data Folder"],data[0]["ExpType"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"],data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_hpc.run_container("single","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
        
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" in data[1]:
            AC_results= AC_hpc.run_container("single","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
            print("AutoCCS finds features through the standard method. \nTarget list specified, annotations will proceed after AutoCCS.")

        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the enhanced method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_hpc.run_container("single","enhanced",False, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
    
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" in data[1]:
            print("AutoCCS finds features through the enhanced method. \nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_hpc.run_container("single","enhanced",True, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"],data[1]["Target List File"], False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])


    # SLIM experiment type workflow execution
    if data[0]["ExpType"] == "SLIM":
        print("Json file passed to Pipeline.py")
        print("SLIM workflow begins execution.")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[1]["mzML Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"],data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method.\nNo Target list specified, annotations will be skipped. ")
            AC_results= AC_hpc.run_container("slim","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False,data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
        if "AC" in data[0]["ToolType"] and "Target List File" in data[1]:
            print("AutoCCS finds features through the standard method.\nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_hpc.run_container("slim","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], data[1]["Metadata File"],False,data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
        

    # Stepped Field experiment type workflow execution
    if data[0]["ExpType"] == "Stepped":
        print("Json file passed to Pipeline.py")
        print("Stepped Field workflow begins execution.")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_hpc.run_container(data[1]["PreProcessed Data Folder"],data[1]["mzML Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_hpc.run_container(data[1]["mzML Data Folder"],data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_hpc.run_container("step","enhanced",True,False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False,False,data[1]["AutoCCS Config File"],data[1]["AutoCCS Results"])
    

    #This required for the GUI to identify which tools were completed.
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results
