#!/usr/bin/env python3.8
import pandas as pd
import numpy as np
import csv


df = pd.read_csv("/tmp/MD/RawFiles_Metadata.csv", sep = ",")

df['SampleType'] = np.where(df['RawFileName'].str.contains('AgTune'),'AgTune','')

df.to_csv("/tmp/MD/RawFiles_Metadata.csv", quoting=csv.QUOTE_ALL, index=False)

