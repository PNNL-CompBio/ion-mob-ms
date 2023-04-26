#!/usr/bin/env python3.7

import fileinput
import argparse



parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-n','--filename', help='File Name of mzML', nargs='?', const='',default='')
parser.add_argument('-t','--tmpname', help='File Name of mzML', nargs='?', const='',default='')
args = vars(parser.parse_args())

FILE_NAME = args["filename"]
TMP_NAME = args["tmpname"]
WITH_LINE_1 = """        <parameter name="Raw data file names"><file>/Work/III_mzML/""" +FILE_NAME + """</file></parameter>"""

WITH_LINE_2 = """ParseDTasRTmzML(1, '/Work/III_mzML/""" + FILE_NAME + """')"""

WITH_LINE_3 = """TMP_FILE_DIRECTORY=/Work/tmp/""" + TMP_NAME

filename_1 = "/Work/MZmine_FeatureFinder-batch.xml"
filename_2 = "/Work/R_PARSE_II.R"
filename_3 = "/MZmine-2.41.2/startMZmine_Linux.sh"

with fileinput.FileInput(filename_1, inplace = True) as f:
    for line in f:
        if("REPLACE_THIS_LINE\n" == line):
            print(WITH_LINE_1,end ='\n')
        else:
            print(line, end ='') 
            
            
with fileinput.FileInput(filename_2, inplace = True) as f:
    for line in f:
        if("RUN_FUNCTION\n" == line):
            print(WITH_LINE_2,end ='\n')
        else:
            print(line, end ='') 


with fileinput.FileInput(filename_3, inplace = True) as f:
    for line in f:
        if("TMP_FILE_DIRECTORY=/Work\n" == line):
            print(WITH_LINE_3,end ='\n')
        else:
            print(line, end ='') 
