

def build_cpu_script(video_dir_input_name,video_dir_output_name, preprocessing_function, amount_cpus = 18, memory = 48, hours = 10, partition = "normal"):
    return f"""#!/bin/bash

#SBATCH --job-name=pp-{video_dir_output_name}
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={amount_cpus}       
#SBATCH --mem={memory}G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition={partition}          # on which partition to submit the job
#SBATCH --time={hours}:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/pp-{video_dir_output_name}.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=jdanel@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/j/jdanel/envs/test

python preprocess_videos.py -source /scratch/tmp/jdanel/data/videos/{video_dir_input_name} -txt mp4_files.txt -save /scratch/tmp/jdanel/data/videos/{video_dir_output_name} -func {preprocessing_function} 
python build_dataset_multithread.py -video_dir_name {video_dir_output_name} -dataset_name {video_dir_output_name}"""

def build_gpu_script(dataset, amount_cpus = 8, memory = 64, hours = 48, partition = "gpu2080"):
    return f"""#!/bin/bash

#SBATCH --job-name=t-{dataset}
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --gres=gpu:4 
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={amount_cpus}       
#SBATCH --mem={memory}G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition={partition}          # on which partition to submit the job
#SBATCH --time={hours}:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/train-{dataset}.dat         # the file where output is written to (stdout & stderr)
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
python train.py -dataset {dataset} -device [0,1,2,3]"""
    
if __name__ == "__main__":
    print(build_gpu_script("o-tf-o"))    
