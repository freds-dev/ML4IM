#!/bin/bash

#SBATCH --job-name=t-test
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --gres=gpu:4 
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8       
#SBATCH --mem=64G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition=gpu2080          # on which partition to submit the job
#SBATCH --time=48:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/train-test.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=jdanel@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/j/jdanel/envs/test

export MKL_SERVICE_FORCE_INTEL=1
python train.py -dataset test -device [0,1,2,3] -project original_validation_split -name 3