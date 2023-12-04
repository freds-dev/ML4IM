#!/bin/bash

#SBATCH --job-name=larger_training
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --gres=gpu:1 
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8       
#SBATCH --mem=20G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition=gpu2080          # on which partition to submit the job
#SBATCH --time=12:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=output_larger_training.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=jdanel@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/j/jdanel/envs/test

python train.py