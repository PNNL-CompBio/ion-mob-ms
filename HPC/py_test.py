#!/usr/bin/python3

"""
py_test.py - Development and Testing Utility Script

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Simple test and development utility script for HPC infrastructure integration.
    Demonstrates inter-process communication via named pipes (FIFOs) for
    asynchronous task execution and status monitoring.
    
    This script serves development and testing purposes, showing how background
    Python processes can be executed and monitored via shell-based named pipes.
    
    Key Features:
    - Named pipe (FIFO)-based inter-process communication
    - Background process execution
    - Development and testing framework
"""

import sys
import os

print("hello this is python")


os.system("""echo 'sudo python3 /vagrant/dev_dockerized/drf/pipeline.py' > /Pipe/mypipe""")
