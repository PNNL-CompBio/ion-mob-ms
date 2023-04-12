#!/usr/bin/env python3.7

import fileinput
import argparse



parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-n','--filename', help='Prefilled Json File path', nargs='?', const='',default='')
args = vars(parser.parse_args())

FILE_NAME = args["filename"]
WITH_LINE = """        <parameter name="Raw data file names"><file>/Work/III_mzML/""" +FILE_NAME + """</file></parameter>"""

#filename = "/people/jaco059/ion-mob-ms/singularity_dev/MZmine_FeatureFinder-batch-two.xml"
filename = "/Work/MZmine_FeatureFinder-batch.xml"

with fileinput.FileInput(filename, inplace = True) as f:
    for line in f:
        if("REPLACE_THIS_LINE\n" == line):
            print(WITH_LINE, end ='\n')
        else:
            print(line, end ='') 
            
            
