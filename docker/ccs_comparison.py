"""
ccs_comparison.py - Collision Cross Section Comparison and Matching Utility

Author: Chang, Christine H <christine.chang@pnnl.gov>
Maintainer: Gosline, Sara <sara.gosline@pnnl.gov>

Description:
    Compares experimental ion mobility mass spectrometry data against reference
    CCS (Collision Cross Section) calibration standards. Performs m/z, drift time,
    and CCS matching against loaded calibration models with configurable error
    tolerances for identification and validation of ion species.
    
    This utility is typically executed within container environments to perform
    post-processing validation and comparison of detected features against
    reference calibration data.
    
    Key Features:
    - Pickle-based CCS calibration model loading
    - HDF5 file format support for ion mobility data
    - Configurable m/z and CCS error tolerances  
    - Peak intensity filtering and quality assessment
    - Pandas-based data manipulation and matching
"""

import pickle

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

