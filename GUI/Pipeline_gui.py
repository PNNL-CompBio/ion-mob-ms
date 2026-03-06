#!/usr/bin/env python3.9
"""
Pipeline_gui.py - Ion Mobility Dashboard Pipeline Orchestration for GUI

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    This module manages the complete analysis workflow for the GUI client.
    It coordinates execution of individual processing tools based on experiment type and configuration.
    Supports three main experiment types: Single field, SLIM, and Stepped field.
    
    Key Features:
    - JSON-based workflow configuration from GUI
    - Support for multiple experiment types (Single, SLIM, Stepped)
    - Flexible tool composition (PW, MZ, DM, AC, PP)
    - Optional feature annotation
    - Workflow result tracking
    - Timestamps for all operations
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
import PW_gui
import MZ_gui
import PP_gui
import DM_gui
import AC_gui
from datetime import datetime



# Container runtime logging with timestamps
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.now(), *args, **kwargs)
print = timestamped_print


def execute_workflow(json_file):
    """
    Execute complete analysis workflow from GUI based on JSON configuration.
    
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


    # Single Field experiment type workflow execution
    if data[0]["ExpType"] == "Single" or data[0]["ExpType"] == "Any":
        print("Json file passed to Pipeline.py")
        print("Single Field workflow begins execution.")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_gui.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_cli.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_gui.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_gui.run_container("single","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
        
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" not in data[1] and "Target List File" in data[1]:
            AC_results= AC_gui.run_container("single","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
            print("AutoCCS finds features through the standard method. \nTarget list specified, annotations will proceed after AutoCCS.")

        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the enhanced method. \nNo Target list specified, annotations will be skipped.")
            AC_results= AC_gui.run_container("single","enhanced",False, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
    
        if "AC" in data[0]["ToolType"] and "IMS Metadata Folder" in data[1] and "Target List File" in data[1]:
            print("AutoCCS finds features through the enhanced method. \nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_gui.run_container("single","enhanced",True, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"],data[1]["Target List File"], False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])


    # SLIM experiment type workflow execution
    if data[0]["ExpType"] == "SLIM":
        print("Json file passed to Pipeline.py")
        print("SLIM workflow begins execution.")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_gui.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            MZ_results = MZ_gui.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"] and "Target List File" not in data[1]:
            print("AutoCCS finds features through the standard method.\nNo Target list specified, annotations will be skipped. ")
            AC_results= AC_gui.run_container("slim","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
        if "AC" in data[0]["ToolType"] and "Target List File" in data[1]:
            print("AutoCCS finds features through the standard method.\nTarget list specified, annotations will proceed after AutoCCS.")
            AC_results= AC_gui.run_container("slim","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
        

    # Stepped Field experiment type workflow execution
    if data[0]["ExpType"] == "Stepped":
        print("Json file passed to Pipeline.py")
        print("Stepped Field workflow begins execution.")
        if "PW" in data[0]["ToolType"]:
            print("Proteowizard converts Files")
            PW_results = PW_gui.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
        # if "DM" in data[0]["ToolType"]:
        #     print("Deimos searches for Features")
        #     DM_results=DM_cli.run_container(data[1]["mzML Data Folder"])
        if "MZ" in data[0]["ToolType"]:
            print("MZMine searches for Features")
            print(data[1]["mzML Data Folder"])
            print(data[1])
            MZ_results = MZ_gui.run_container(data[1]["mzML Data Folder"])
        if "AC" in data[0]["ToolType"]:
            print("AutoCCS finds features through the enhanced method.")
            AC_results= AC_gui.run_container("step","enhanced",True,False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False,False,data[1]["AutoCCS Config File"])
    

    #This required for the GUI to identify which tools were completed.
    all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    return all_results
