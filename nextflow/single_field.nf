/*
 * Step 1. using pnnl_processor, perform frame summing and smoothing
 */

params.agilent_dir = "/mnt/anubhav_MSSHARE/autoccs/data/test-data/SingleField/I_Raw/AgTune_01_msms_POS_01Dec20_Fiji_Infusion_Min50.d"

agilent = file(params.agilent_dir)

process pnnlProcessor {

    container params.container_pnnl_preprocessor

    input:
    file data from agilent

    // output:
    // path II_Preprocessed
    """
    wine /PNNL-Preprocessor_4.0_2022.02.17/PNNL-PreProcessor.exe \
    -smooth \
    -driftKernel 1 \
    -lcKernel 0  \
    -minIntensity 20 \
    -split \
    -r \
    -dataset ${data}
    """
}