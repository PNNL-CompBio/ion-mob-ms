import pickle

import deimos
import pandas as pd
import os
import argparse

# Author: Chang, Christine H <christine.chang@pnnl.gov>
# Maintainer: Gosline, Sara <sara.gosline@pnnl.gov>

# set match error tolerances
ERR_MZ = 100.0e-6
ERR_CCS = 0.010


def comparison(file_a, file_b, ccs_file):

    # load CCS calibration to generate CCS column
    with open(
        ccs_file,
        "rb",
    ) as f:
        tune = pickle.load(f)

    # load reference file containing mz and compute ccs
    df_a = deimos.load_hdf(file_a)
    df_a["ccs"] = [
        tune.arrival2ccs(mz, dt) for mz, dt in zip(df_a["mz"], df_a["drift_time"])
    ]
    df_a = df_a[df_a["sum_4"] > 5000].reset_index(drop=True)

    # load comparison file and compute associated ccs
    df_b = deimos.load_hdf(
        file_b,
        key="ms2",
    )
    df_b["ccs"] = [
        tune.arrival2ccs(mz, dt) for mz, dt in zip(df_b["mz"], df_b["drift_time"])
    ]

    # iteratively find matches within defined (mz, ccs) parameters
    matches = list()
    for i, (mz, ccs) in enumerate(zip(df_a["mz"].values[:10], df_a["ccs"].values[:10])):

        # calculate tolerances given relative errors
        tol_mz, tol_ccs = ERR_MZ * mz, ERR_CCS * ccs

        # search df_b for matching mz, ccs feature
        tmp = deimos.locate(
            df_b, by=["mz", "ccs"], loc=[mz, ccs], tol=[tol_mz, tol_ccs]
        )

        # annotate with reference (db_a) index
        if tmp is not None:
            tmp["i_match"] = i
        matches.append(tmp)

    # collate any matches found within given parameters
    matches = pd.concat(matches, ignore_index=True)

    return matches


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser('This script runs CCS comparison')
    parser.add_argument('ccsFile',help='CCS file')
    parser.add_argument('fileA',help='File A')
    parser.add_argument('fileB',help='File B')

    args = parser.parse_args()

    # define file paths
    if len(args)!=3:
        sys.exit("Need three file arguments")
    
    ccs_file = args.ccsFile#os.path.join(os.environ.get("CCS_FILE"))
    file_a = args.fileA#os.path.join(os.environ.get("FILE_A"))
    file_b = args.fileB#os.path.join(os.environ.get("FILE_B"))

    matches = comparison(file_a, file_b, ccs_file)

    save_at = os.path.join(os.environ.get("SAVE_AT"))

    match_file_path = os.path.join(save_at, f"matches.csv")
    matches.to_csv(match_file_path, sep=",")

