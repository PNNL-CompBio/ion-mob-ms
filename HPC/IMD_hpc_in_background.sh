#!/bin/csh
#SBATCH -A Ion_Mob_Dashboard
#SBATCH -t 1
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -J IMD_Dorrestein_stepped
#SBATCH -o IMD_Dorrestein_stepped_output.txt
#SBATCH -e IMD_Dorrestein_stepped_error.txt




module load singularity
module load python/3.7.0


python3 CLI_hpc.py --json sample.json
