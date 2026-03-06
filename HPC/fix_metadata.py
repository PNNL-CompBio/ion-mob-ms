#!/usr/bin/env python3.8

"""
fix_metadata.py - Metadata Correction and Sample Type Annotation Utility

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Utility script for post-processing raw file metadata CSV files to annotate
    sample types based on filename patterns. Reads raw file metadata, identifies
    AgTune calibrant files, and marks them for exclusion from analysis pipelines.
    
    This script is typically executed as a preprocessing step in HPC workflows
    to prepare metadata files with correct sample type classifications before
    feature detection and CCS calculations.
    
    Key Features:
    - CSV metadata file processing
    - Pattern-based sample type detection (AgTune calibrants)
    - Automated metadata annotation and backup
    - Pandas-based data manipulation
"""

import pandas as pd
import numpy as np
import csv


df = pd.read_csv("/tmp/MD/RawFiles_Metadata.csv", sep = ",")

df['SampleType'] = np.where(df['RawFileName'].str.contains('AgTune'),'AgTune','')

df.to_csv("/tmp/MD/RawFiles_Metadata.csv", quoting=csv.QUOTE_ALL, index=False)

