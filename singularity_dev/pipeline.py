#!/usr/bin/python3

from minio import Minio
# from minio.error import ResponseError
# import urllib3
import json
import ast
import PW_web
import MZ_web

def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.

    print("looking for client.")

    client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    print("client up")
    found = client.bucket_exists("ion-mob-upload")
    if not found:
        print("ion-mob-upload not found")
    else:
        print("ion-mob-upload found")

    exp_details = client.get_object("ion-mob-upload", "JSON_metadata")
    exp_details = exp_details.data.decode("utf-8")
    exp_details = exp_details.replace("\'", "\"")
    exp_details = exp_details.replace("None", '"False"')
    data = json.loads(exp_details) 

    print(data["ExperimentType"])
    
    
    if not data["ExperimentType"]:
        print("No Experiment type found")
        steps = "None"
    elif data["ExperimentType"] in ["SIF", "STF", "SLIM"]:
        steps = ["PW", "MZ", "AC"]
    else: 
        steps = data["ExperimentType"]

    print("Steps to run are:", steps)


    if "PW" in steps:
        print("Running ProteoWizard")
    #         print("Proteowizard converts Files")
    #         PW_results = PW_step.run_container("data["ExpType"]")
        PW_web.run()

    if "MZ" in steps:
        print("Running Mzmine")
    #         print("Proteowizard converts Files")
    #         PW_results = PW_step.run_container("data["ExpType"]")
        MZ_web.run()
    
######### Old pipeline

    ## Single Field
    # if data["ExperimentType"] == "SIF":
    #     print("Json file passed to Pipeline.py")
    #     print("Single Field Begins here.")
    #     # if "PP" in steps:
    #     #     print("PNNL Preprocessor does Filtering and Smoothing")
    #         # PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
    #     if "PW" in steps:
    #         print("Proteowizard converts Files")
    #         PW_results = PW_step.run_container("data["ExpType"]")
    #     if "DM" in steps:
    #         print("Deimos searches for Features")
    #         DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
    #     if "MZ" in steps:
    #         print("MZMine searches for Features")
    #         print(data[1]["mzML Data Folder"])
    #         print(data[1])
    #         MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
    #     if "AC" in steps and "IMS Metadata Folder" not in data[1] and "Target List File" not in data[1]:
    #         print("AutoCCS finds features through the standard method. \nNo Target list specified, annotations will be skipped.")
    #         AC_results= AC_step.run_container("single","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
        
    #     if "AC" in steps and "IMS Metadata Folder" not in data[1] and "Target List File" in data[1]:
    #         AC_results= AC_step.run_container("single","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], False, data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
    #         print("AutoCCS finds features through the standard method. \nTarget list specified, annotations will proceed after AutoCCS.")

    #     if "AC" in steps and "IMS Metadata Folder" in data[1] and "Target List File" not in data[1]:
    #         print("AutoCCS finds features through the enhanced method. \nNo Target list specified, annotations will be skipped.")
    #         AC_results= AC_step.run_container("single","enhanced",False, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], False, False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])
    
    #     if "AC" in steps and "IMS Metadata Folder" in data[1] and "Target List File" in data[1]:
    #         print("AutoCCS finds features through the enhanced method. \nTarget list specified, annotations will proceed after AutoCCS.")
    #         AC_results= AC_step.run_container("single","enhanced",True, data[1]["Calibrant File"], data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"],data[1]["Target List File"], False,data[1]["PreProcessed Data Folder"],data[1]["AutoCCS Config File"])


    # ## Slim 
    # elif data["ExperimentType"] == "SLIM":
    #     print("Json file passed to Pipeline.py")
    #     print("SLIM Begins here.")
    #     # if data[1]["Experiment"]
    #     if "PP" in steps:
    #         print("PNNL Preprocessor does Filtering and Smoothing")
    #         PP_results = PP_step.run_container(data[1]["Raw Data Folder"],data[0]["DriftKernel"],data[0]["LCKernel"],data[0]["MinIntensity"])
    #     if "PW" in steps:
    #         print("Proteowizard converts Files")
    #         PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
    #     if "DM" in steps:
    #         print("Deimos searches for Features")
    #         DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
    #     if "MZ" in steps:
    #         print("MZMine searches for Features")
    #         MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
    #     if "AC" in steps and "Target List File" not in data[1]:
    #         print("AutoCCS finds features through the standard method.\nNo Target list specified, annotations will be skipped. ")
    #         AC_results= AC_step.run_container("slim","standard",False, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], False, data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
    #     if "AC" in steps and "Target List File" in data[1]:
    #         print("AutoCCS finds features through the standard method.\nTarget list specified, annotations will proceed after AutoCCS.")
    #         AC_results= AC_step.run_container("slim","standard",True, data[1]["Calibrant File"],False, data[1]["Feature Data Folder"], data[1]["Target List File"], data[1]["Metadata File"],False,data[1]["AutoCCS Config File"])
        

    # ## Stepped Field
    # elif data["ExperimentType"] == "STF":
    #     print("Json file passed to Pipeline.py")
    #     print("Stepped Field Begins here.")
    #     # if data[1]["Experiment"]
    #     if "PP" in steps:
    #         print("PNNL Preprocessor does Filtering and Smoothing")
    #     if "PW" in steps:
    #         print("Proteowizard converts Files")
    #         PW_results = PW_step.run_container(data[1]["PreProcessed Data Folder"],data[0]["ExpType"])
    #     if "DM" in steps:
    #         print("Deimos searches for Features")
    #         DM_results=DM_step.run_container(data[1]["mzML Data Folder"])
    #     if "MZ" in steps:
    #         print("MZMine searches for Features")
    #         print(data[1]["mzML Data Folder"])
    #         print(data[1])
    #         MZ_results = MZ_step.run_container(data[1]["mzML Data Folder"])
    #     if "AC" in steps:
    #         print("AutoCCS finds features through the enhanced method.")
    #         AC_results= AC_step.run_container("step","enhanced",False,False, data[1]["IMS Metadata Folder"], data[1]["Feature Data Folder"], data[1]["Target List File"], False,False,data[1]["AutoCCS Config File"])
    

    # #This required for the GUI to identify which tools were completed.
    # all_results = [PP_results, PW_results, MZ_results, DM_results, AC_results]
    # return all_results

######### Old pipeline























if __name__ == "__main__":
    try:
        main()
    except:
        print("failed")
        pass
    # except S3Error as exc:
    #     print("error occurred.", exc)
