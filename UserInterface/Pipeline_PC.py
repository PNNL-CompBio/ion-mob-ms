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
    os.chdir(cur_dir) # change working directory
    f = open(json_file)
    data = json.load(f)
    f.close()

    ## Single Field
    if data[0]["Experiment"] == 0:
        print("Single Field Begins here.")


    ## Slim 
    if data[0]["Experiment"] == 1:
        print("SLIM Begins here.")


    ## Stepped Field
    #Define all variables
    # for me : -output_dir "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/docker_test_area/AC_python_area/IV_Results" -mode "multi" 
    #config_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/autoCCS_config.xml"
    # framemeta_files = "/Users/jaco059/OneDrive\ -\ PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/IV_ImsMetadata/*.txt"
    # target_list_file = "/Users/jaco059/OneDrive - PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/TargetList_NeutralMass.csv"
    # feature_files = "/Users/jaco059/OneDrive\ -\ PNNL/Desktop/IonMobility_Desktop_App_Front_End/ion-mob-ms/test-data/SteppedField/IV_Features_csv/*.csv"



    #Run pipeline
    if data[0]["Experiment"] == 2:
        print("Stepped Field Begins here.")
        # if data[1]["Experiment"]
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
            #data[3]["FrameMetadata"] = (data[3]["FrameMetadata"]).replace(" ", "\ ")
            #data[3]["Feature Data"] = (data[3]["Feature Data"]).replace(" ", "\ ")
            AC_step_PC.run_container(data[3]["FrameMetadata"], data[3]["Feature Data"], data[3]["Target List"])

