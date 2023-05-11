#!/bin/csh
#SBATCH -A IMD_Dev
#SBATCH -t 3-6
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -J IMD_Dorrestein_stepped
#SBATCH -o IMD_Dorrestein_stepped_output.txt
#SBATCH -e IMD_Dorrestein_stepped_error.txt




module load singularity
module load python/3.7.0
#echo "FIRST"
#ls /rcfs/projects/IMD_IMD_Dev
#echo "SECOND"
#ls /rcfs/projects/IMD_IMD_Processing


python3 CLI_hpc.py --json sample.json_testing
