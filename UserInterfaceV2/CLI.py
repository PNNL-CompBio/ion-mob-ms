#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

import argparse
import subprocess
import sys
# import docker
import os
import tarfile
import time
import platform
import Pipeline_V2
import PW_step
import MZ_step
import PP_step
import DM_step
import AC_step
import json


# possible_files = ["Raw Data Folder",
#                   "PreProcessed Data Folder",
#                   "Feature Data Folder",
#                   "IMS Metadata Folder",
#                   "IMS Metadata Folder (optional)",
#                         "Calibrant File",
#                         "Target List File",
#                         "Target List File (optional)",
#                         "Metadata File",
#                         "mzML Data Folder",
#                         "AutoCCS Config File"]


if __name__ == '__main__':
    
    
    file_dict = dict()
    param_dict = dict()

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-j','--json', help='Prefilled Json File path', nargs='?', const='',default='')
    parser.add_argument('-n','--ExpName', help='Experiment name', nargs='?', const='',default='')
    parser.add_argument('-e','--ExpType', help='Experiment type', nargs='?', const='',default='')
    parser.add_argument('-t','--ToolType', help='Tool Type as list', nargs='*')
    parser.add_argument('-r','--Raw', help='Raw Data Folder', nargs='?', const='',default='')
    parser.add_argument('-p','--PP', help='PreProcessed Data Folder', nargs='?', const='',default='')
    parser.add_argument('-m','--mzML', help='mzML Data Folder', nargs='?', const='',default='')
    parser.add_argument('-f','--FF', help='Feature Data Folder', nargs='?', const='',default='')
    parser.add_argument('-i','--IMSMeta', help='IMS Metadata Folder', nargs='?', const='',default='')
    parser.add_argument('-d','--IMSMetaopt', help='IMS Metadata Folder (optional)', nargs='?', const='',default='')
    parser.add_argument('-a','--ACConfig', help='AutoCCS Config File', nargs='?', const='',default='')
    parser.add_argument('-s','--TLF', help='Target List File', nargs='?', const='',default='')
    parser.add_argument('-q','--TLFopt', help='Target List File (optional)', nargs='?', const='',default='')
    parser.add_argument('-z','--MetadataFile', help='Metadata File', nargs='?', const='',default='')
    parser.add_argument('-c','--Calibrant', help='Calibrant File', nargs='?', const='',default='')

    args = vars(parser.parse_args())


    #write json file using parparse inputs


    #individual tools
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
            if args["PP"] != '' and args["IMSMetaopt"] != '' and args["FF"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["TLFopt"] != '':
                file_dict["PreProcessed Data Folder"] = args["PP"]
                file_dict["IMS Metadata Folder (optional)"] = args["IMSMetaopt"]
                file_dict["Feature Data Folder"] = args["FF"]
                file_dict["Calibrant File"] = args["Calibrant"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File (optional)"] = args["TLFopt"]
            else: 
                sys.exit("Missing required file(s)")
                
        if args["ExpType"] == "SLIM":
            if args["FF"] != '' and args["MetadataFile"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["TLFopt"] != '':
                file_dict["Feature Data Folder"] = args["FF"]
                file_dict["Metadata File"] = args["MetadataFile"]
                file_dict["Calibrant File"] = args["Calibrant"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File (optional)"] = args["TLFopt"]
            else: 
                sys.exit("Missing required file(s)")
            
        if args["ExpType"] == "Stepped":
            if args["FF"] != '' and args["IMSMeta"] != '' and args["ACConfig"] != '' and args["TLF"] != '':
                file_dict["Feature Data Folder"] = args["FF"]
                file_dict["IMS Metadata Folder"] = args["IMSMeta"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File"] = args["TLF"]
            else: 
                sys.exit("Missing required file(s)")
            
        
    #workflows
    if len(args["ToolType"]) > 1:
        if args["ExpType"] == "Single":
            if args["PP"] != '' and args["IMSMetaopt"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["TLFopt"] != '':
                file_dict["PreProcessed Data Folder"] = args["PP"]
                file_dict["IMS Metadata Folder (optional)"] = args["IMSMetaopt"]
                file_dict["Calibrant File"] = args["Calibrant"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File (optional)"] = args["TLFopt"]
                #tmp folders
                file_dict["mzML Data Folder"] = os.path.join(os.path.dirname(__file__),"III_mzML")
                file_dict["Feature Data Folder"] =os.path.join(os.path.dirname(__file__),"IV_Features_csv","*.csv")
            else: 
                sys.exit("Missing required file(s)")

        if args["ExpType"] == "SLIM":
            if args["PP"] != '' and args["MetadataFile"] != '' and args["Calibrant"] != '' and args["ACConfig"] != '' and args["TLFopt"] != '':
                file_dict["PreProcessed Data Folder"] = args["PP"]
                file_dict["Metadata File"] = args["MetadataFile"]
                file_dict["Calibrant File"] = args["Calibrant"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File (optional)"] = args["TLFopt"]
                #tmp folders
                file_dict["mzML Data Folder"] = os.path.join(os.path.dirname(__file__),"III_mzML")
                file_dict["Feature Data Folder"] =os.path.join(os.path.dirname(__file__),"IV_Features_csv","*.csv")
            else: 
                sys.exit("Missing required file(s)")
                
        if args["ExpType"] == "Stepped":
            if args["PP"] != '' and args["IMSMeta"] != '' and args["ACConfig"] != '' and args["TLF"] != '':
                file_dict["PreProcessed Data Folder"] = args["PP"]
                file_dict["IMS Metadata Folder"] = args["IMSMeta"]
                file_dict["AutoCCS Config File"] = args["ACConfig"]
                file_dict["Target List File"] = args["TLF"]
                #tmp folders
                file_dict["mzML Data Folder"] = os.path.join(os.path.dirname(__file__),"III_mzML")
                file_dict["Feature Data Folder"] =os.path.join(os.path.dirname(__file__),"IV_Features_csv","*.csv")
            else: 
                sys.exit("Missing required file(s)")


    param_dict["ExpName"] = args["ExpName"]
    param_dict["ExpType"] = args["ExpType"]
    param_dict["ToolType"] = args["ToolType"]



    print("\n")
    print("file dict:", file_dict)
    print("\n")
    print("param dict:", param_dict)
    print("\n")



    json_export = [param_dict,file_dict]
    json_object = json.dumps(json_export, indent = 4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


    Pipeline_V2.execute_workflow("sample.json")

