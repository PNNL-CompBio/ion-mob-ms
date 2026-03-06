#!/usr/bin/python3

"""
pipeline.py - MinIO-based Workflow Orchestration Pipeline

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Orchestrates mass spectrometry analysis workflows using MinIO S3-compatible
    object storage as the data backend. Manages workflow resources, coordinates
    tool execution, and handles result collection from distributed processing
    infrastructure. This module is in development and subject to architectural changes.
    
    This module integrates MinIO storage with HPC processing tools (Proteowizard
    and MZmine web modules) to enable scalable cloud-based analysis pipelines
    with persistent data storage and result tracking.
    
    Key Features:
    - MinIO bucket management for data organization
    - Workflow coordination with remote storage backends
    - Integration with PW_web and MZ_web processing modules
    - Result retrieval and organization from object storage
    
    Development Status: In active development - API and functionality subject to change
"""

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
        MZ_web.run()

if __name__ == "__main__":
    try:
        main()
    except:
        print("failed")
        pass


















if __name__ == "__main__":
    try:
        main()
    except:
        print("failed")
        pass
    # except S3Error as exc:
    #     print("error occurred.", exc)
