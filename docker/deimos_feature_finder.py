#!/usr/bin/env python3.7

"""
deimos_feature_finder.py - Deimos Persistent Homology Feature Detection

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Container-internal utility script for Deimos persistent homology-based
    feature detection on ion mobility mass spectrometry mzML data files.
    Processes individual mzML files within container environment, applies
    persistent homology peak picking, and exports detected features in
    MZmine-compatible CSV format.
    
    This script is designed for execution within Docker/Singularity containers
    where individual mzML files are mounted and processed in isolation.
    Enforces single MS level per file constraint for consistent processing.
    
    Key Features:
    - Deimos persistent homology peak detection
    - Single MS-level file validation
    - HDF5 mzML file loading and processing
    - MZmine-compatible CSV output formatting
    - Automatic feature meta-data assignment
"""

import deimos
import os
for file in os.listdir("/III_mzML"):
    if file.endswith(".mzML"):
        path_to_mzml = "/III_mzML/" + file
        file_name = file
        output_path = "/IV_Features_csv/" + file + "_c_dc_de.csv"
#this above output suffix is used to match mzmine


data = deimos.load(path_to_mzml, accession={'drift_time': 'MS:1002476'})

data_list = list(data.keys())
if len(data_list) > 1:
    print("Deimos failed to run.\n Each file may only contain one MS level.\n Files must be seperated using PNNL PreProcessesor first.")
else:
    peaks = deimos.peakpick.persistent_homology(data[data_list[0]], dims=['mz', 'drift_time'])
    peaks.rename(columns={'drift_time':'Peak RT'}, inplace=True)
    peaks.rename(columns={'intensity':'Peak area'}, inplace=True)
    peaks.rename(columns={'mz':'Peak m/z'}, inplace=True)
    peaks['row ID'] = peaks.index
    peaks['Peak height'] = peaks['Peak area']
    peaks.insert(1, 'Peak charge', '1')

#these above columns are modified to match mzMine format (required for autoCCS)

    peaks.to_csv(output_path, index=False)



