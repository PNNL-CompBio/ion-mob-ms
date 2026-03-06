#!/usr/bin/env python3.9
"""
Pipeline_cli.py - Ion Mobility Dashboard Pipeline Orchestration Module

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module manages the complete analysis workflow for ion mobility mass spectrometry data.
    It coordinates execution of individual processing tools based on experiment type and user configuration.
    Supports three main experiment types: Single field, SLIM, and Stepped field.
    
    Key Features:
    - JSON-based workflow configuration
    - Support for multiple experiment types (Single, SLIM, Stepped)
    - Flexible tool composition (PW, MZ, DM, AC, PP)
    - Optional feature annotation
    - Workflow result tracking and reporting
    - Timestamps for all operations
    
    Experiment Types:
    - Single Field (SIF): Automated metadata extraction from raw data
    - SLIM: User-provided metadata, simplified processing
    - Stepped Field (STF): Ion mobility-resolved processing with frame metadata
"""

import argparse
import json
import subprocess
import sys
import docker
import os
import tarfile
import time
import platform
import PW_cli
import MZ_cli
import PP_cli
import DM_cli
import AC_cli
from datetime import datetime



# Runtime logging with timestamps for execution tracking
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print


def execute_workflow(json_file):
    """
    Execute complete analysis workflow based on JSON configuration.
    
    Parameters:
        json_file (str): Path to JSON file containing workflow configuration
        
    Returns:
        list: Results from each processing step [PP, PW, MZ, DM, AC]
    """
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


    # Single Field experiment workflow
    if data[0]["ExpType"] == "Single" or data[0]["ExpType"] == "Any":
        print("Single field experiment workflow initiated")
        if "PW" in data[0]["ToolType"]:
            print("Step 1: Proteowizard converting raw files to mzML format")
            PW_results = PW_cli.run_container(data[1]["PreProcessed Data Folder"], data[1]["mzML Data Folder"], data[0]["ExpType"])
        if "MZ" in data[0]["ToolType"]:
            print("Step 2: MZmine detecting features from mzML files")
            MZ_results = MZ_cli.run_container(data[1]["mzML Data Folder"], data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" not in data[1]:
            print("Step 3: AutoCCS standard method (no metadata or annotation)")
            AC_results = AC_cli.run_container("single", "standard", False, data[1]["Calibrant File"], False, 
                                             data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"],
                                             data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])
        
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" in data[1]:
            print("Step 3: AutoCCS standard method with annotation")
            AC_results = AC_cli.run_container("single", "standard", True, data[1]["Calibrant File"], False, 
                                             data[1]["Feature Data Folder"], data[1]["Target List File"], False, 
                                             data[1]["PreProcessed Data Folder"], data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])

        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" not in data[1]:
            print("Step 3: AutoCCS enhanced method with frame metadata (no annotation)")
            AC_results = AC_cli.run_container("single", "enhanced", False, data[1]["Calibrant File"], 
                                             data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,
                                             data[1]["PreProcessed Data Folder"], data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])
    
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" in data[1]:
            print("Step 3: AutoCCS enhanced method with frame metadata and annotation")
            AC_results = AC_cli.run_container("single", "enhanced", True, data[1]["Calibrant File"], 
                                             data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"],
                                             data[1]["Target List File"], False, data[1]["PreProcessed Data Folder"],
                                             data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])

    # SLIM experiment workflow
    if data[0]["ExpType"] == "SLIM":
        print("SLIM experiment workflow initiated")
        if "PW" in data[0]["ToolType"]:
            print("Step 1: Proteowizard converting raw files to mzML format")
            PW_results = PW_cli.run_container(data[1]["PreProcessed Data Folder"], data[1]["mzML Data Folder"], data[0]["ExpType"])
        if "MZ" in data[0]["ToolType"]:
            print("Step 2: MZmine detecting features from mzML files")
            MZ_results = MZ_cli.run_container(data[1]["mzML Data Folder"], data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"] and "Target List File" not in data[1]:
            print("Step 3: AutoCCS standard method with user metadata (no annotation)")
            AC_results = AC_cli.run_container("slim", "standard", False, data[1]["Calibrant File"], False, 
                                             data[1]["Feature Data Folder"], False, data[1]["Metadata File"], False,
                                             data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])
        if "AC" in data[0]["ToolType"] and "Target List File" in data[1]:
            print("Step 3: AutoCCS standard method with user metadata and annotation")
            AC_results = AC_cli.run_container("slim", "standard", True, data[1]["Calibrant File"], False, 
                                             data[1]["Feature Data Folder"], data[1]["Target List File"], data[1]["Metadata File"],
                                             False, data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])
        
    # Stepped Field experiment workflow
    if data[0]["ExpType"] == "Stepped":
        print("Stepped field experiment workflow initiated")
        if "PW" in data[0]["ToolType"]:
            print("Step 1: Proteowizard converting raw files to mzML format")
            PW_results = PW_cli.run_container(data[1]["PreProcessed Data Folder"], data[1]["mzML Data Folder"], data[0]["ExpType"])
        if "MZ" in data[0]["ToolType"]:
            print("Step 2: MZmine detecting features from mzML files")
            MZ_results = MZ_cli.run_container(data[1]["mzML Data Folder"], data[1]["Feature Data Folder"])
        if "AC" in data[0]["ToolType"]:
            print("Step 3: AutoCCS enhanced multi-level method with frame metadata")
            AC_results = AC_cli.run_container("step", "enhanced", True, False, data[1]["IMS Metadata Folder"], 
                                             data[1]["Feature Data Folder"], data[1]["Target List File"], False, False,
                                             data[1]["AutoCCS Config File"], data[1]["AutoCCS Results"])
    
    # Track and return results from all processing steps
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results