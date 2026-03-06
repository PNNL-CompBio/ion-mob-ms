#!/usr/bin/env python3.9
"""
CLI.py - Ion Mobility Dashboard Command Line Interface

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Main command-line interface entry point for the Ion Mobility Dashboard (IMD).
    Provides argument parsing and workflow orchestration for ion mobility mass spectrometry
    data processing. Supports both individual tool execution and complete analysis pipelines.
    
    Key Features:
    - Command-line argument parsing for all tool inputs
    - JSON-based workflow configuration
    - Support for single experiments and complete pipelines
    - Integration with all data processing modules (PW, MZ, DM, AC, PP)
    - Cross-platform compatibility
    """

import argparse
import subprocess
import sys
import os
import tarfile
import time
import platform
import Pipeline_cli
import PW_cli
import MZ_cli
import PP_cli
import DM_cli
import AC_cli
import json

if __name__ == '__main__':
    print("Ion Mobility Dashboard Command Line Interface Starting")
    file_dict = dict()
    param_dict = dict()

    # Configure command-line argument parser
    parser = argparse.ArgumentParser(description='Ion Mobility Dashboard - CLI for mass spectrometry data processing')
    parser.add_argument('-j', '--json', help='Prefilled JSON configuration file path', nargs='?', const='', default='')
    parser.add_argument('-n', '--ExpName', help='Experiment name', nargs='?', const='', default='')
    parser.add_argument('-e', '--ExpType', help='Experiment type (Single, SLIM, Stepped)', nargs='?', const='', default='')
    parser.add_argument('-t', '--ToolType', help='Tools to execute (PW, MZ, DM, AC, PP)', nargs='*')
    parser.add_argument('-r', '--Raw', help='Raw data folder path', nargs='?', const='', default='')
    parser.add_argument('-p', '--PP', help='Preprocessed data folder path', nargs='?', const='', default='')
    parser.add_argument('-m', '--mzML', help='mzML data folder path', nargs='?', const='', default='')
    parser.add_argument('-f', '--FF', help='Feature data folder path', nargs='?', const='', default='')
    parser.add_argument('-i', '--IMSMeta', help='IMS metadata folder path', nargs='?', const='', default='')
    parser.add_argument('-a', '--ACConfig', help='AutoCCS configuration file path', nargs='?', const='', default='')
    parser.add_argument('-s', '--TLF', help='Target list file path', nargs='?', const='', default='')
    parser.add_argument('-z', '--MetadataFile', help='Metadata file path', nargs='?', const='', default='')
    parser.add_argument('-c', '--Calibrant', help='Calibrant file path', nargs='?', const='', default='')
    parser.add_argument('-o', '--AutoCCS', help='AutoCCS output results directory', nargs='?', const='', default='')
    args = vars(parser.parse_args())

    # Process JSON configuration file if provided
    if args["json"] != '':
        print("JSON configuration file provided. Starting workflow")
        Pipeline_cli.execute_workflow(args["json"])
        print("Workflow completed successfully")
    
    # Build and execute individual tool workflows from command-line arguments
    else:
        if args["ToolType"] == ["PW"]:
            if args["PP"] != '':
                file_dict["PreProcessed Data Folder"] = args["PP"]
            else: 
                sys.exit("Missing required file(s)")
            
        if args["ToolType"] == ["MZ"]:
            if args["MZ"] != '':
                file_dict["mzML Data Folder"] = args["MZ"]
            else: 
                sys.exit("Missing required file(s)")
                
        if args["ToolType"] == ["DM"]:
            if args["MZ"] != '':
                file_dict["mzML Data Folder"] = args["MZ"]
            else: 
                sys.exit("Missing required file(s)")
                
        if args["ToolType"] == ["AC"]:
            if args["ExpType"] == "Single":
                if args["PP"] != '' and args["FF"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["AutoCCS"] != '':
                    file_dict["PreProcessed Data Folder"] = args["PP"]
                    file_dict["IMS Metadata Folder (optional)"] = os.path.join(args["IMSMeta"])
                    file_dict["Feature Data Folder"] = os.path.join(args["FF"])
                    file_dict["Calibrant File"] = args["Calibrant"]
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                    if args["TLF"] != '':
                        file_dict["Target List File (optional)"] = args["TLF"]
                    if args["IMSMeta"] != '':
                        file_dict["IMS Metadata Folder (optional)"] = os.path.join(args["IMSMeta"])
                else: 
                    sys.exit("Missing required file(s)")
                    
            if args["ExpType"] == "SLIM":
                if args["FF"] != '' and args["MetadataFile"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["AutoCCS"] != '':
                    file_dict["Feature Data Folder"] = os.path.join(args["FF"])
                    file_dict["Metadata File"] = args["MetadataFile"]
                    file_dict["Calibrant File"] = args["Calibrant"]
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                    if args["TLF"] != '':
                        file_dict["Target List File (optional)"] = args["TLF"]
                else: 
                    sys.exit("Missing required file(s)")
                
            if args["ExpType"] == "Stepped":
                if args["FF"] != '' and args["IMSMeta"] != '' and args["ACConfig"] != '' and args["TLF"] != '' and args["AutoCCS"] != '':
                    file_dict["Feature Data Folder"] = os.path.join(args["FF"])
                    file_dict["IMS Metadata Folder"] = os.path.join(args["IMSMeta"])
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["Target List File"] = args["TLF"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                else: 
                    sys.exit("Missing required file(s)")
                
            
        #workflows
        if len(args["ToolType"]) > 1:
            if args["ExpType"] == "Single":
                if args["PP"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["AutoCCS"] != '' and args["mzML"] != '' and args["FF"] != '':
                    file_dict["PreProcessed Data Folder"] = args["PP"]
                    file_dict["Calibrant File"] = args["Calibrant"]
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                    file_dict["mzML Data Folder"] = args["mzML"]
                    file_dict["Feature Data Folder"] =args["FF"]
                    if args["TLF"] != '':
                        file_dict["Target List File (optional)"] = args["TLF"]
                    if args["IMSMeta"] != '':
                        file_dict["IMS Metadata Folder (optional)"] = os.path.join(args["IMSMeta"])
                else: 
                    sys.exit("Missing required file(s)")

            if args["ExpType"] == "SLIM":
                if args["PP"] != '' and args["MetadataFile"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["AutoCCS"] != '' and args["mzML"] != '' and args["FF"] != '':
                    file_dict["PreProcessed Data Folder"] = args["PP"]
                    file_dict["Metadata File"] = args["MetadataFile"]
                    file_dict["Calibrant File"] = args["Calibrant"]
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                    file_dict["mzML Data Folder"] = args["mzML"]
                    file_dict["Feature Data Folder"] =args["FF"]
                    if args["TLF"] != '':
                        file_dict["Target List File (optional)"] = args["TLF"]
                  
                else: 
                    sys.exit("Missing required file(s)")
                    
            if args["ExpType"] == "Stepped":
                if args["PP"] != '' and args["IMSMeta"] != '' and args["ACConfig"] != '' and args["TLF"] != '' and args["AutoCCS"] != '' and args["mzML"] != '' and args["FF"] != '':
                    file_dict["PreProcessed Data Folder"] = args["PP"]
                    file_dict["IMS Metadata Folder"] =  os.path.join(args["IMSMeta"])
                    file_dict["AutoCCS Config File"] = args["ACConfig"]
                    file_dict["Target List File"] = args["TLF"]
                    file_dict["AutoCCS Results"] = args["AutoCCS"]
                    file_dict["mzML Data Folder"] = args["mzML"]
                    file_dict["Feature Data Folder"] =args["FF"]
                else: 
                    sys.exit("Missing required file(s)")


        param_dict["ExpName"] = args["ExpName"]
        param_dict["ExpType"] = args["ExpType"]
        param_dict["ToolType"] = args["ToolType"]




        json_export = [param_dict,file_dict]
        json_object = json.dumps(json_export, indent = 4)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)

        Pipeline_cli.execute_workflow("sample.json")


        print("Command Line Interface Has Completed")