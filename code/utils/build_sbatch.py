import argparse
import os
from helper import whoami

def write_file(path,content):
    # If dir is not exisitng just create it:
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    f = open(path, "w")
    f.write(content)
    f.close()
    print(f"Saved content to {path}")

def build_cpu_script(video_dir_input_name,video_dir_output_name, preprocessing_function, amount_cpus = 18, memory = 48, hours = 10, partition = "normal"):
    user = whoami()
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
#SBATCH --mail-user={user}@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/{user[0]}/{user}/envs/test

python preprocess_videos.py -source /scratch/tmp/{user}/data/videos/{video_dir_input_name} -txt mp4_files.txt -save /scratch/tmp/{user}/data/videos/{video_dir_output_name} -func {preprocessing_function} 
python build_dataset_multithread.py -video_dir_name {video_dir_output_name} -dataset_name {video_dir_output_name}"""

def build_gpu_script(dataset, index = "first_run",project_name= "", amount_cpus = 8, memory = 64, hours = 96, partition = "gpu2080,gputitanrtx,gpua100,gpuhgx"):
    user = whoami()
    return f"""#!/bin/bash

#SBATCH --job-name=t-{project_name}-{dataset}
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --gres=gpu:4 
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={amount_cpus}       
#SBATCH --mem={memory}G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition={partition}          # on which partition to submit the job
#SBATCH --time={hours}:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/{project_name}/train/{dataset}.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user={user}@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/{user[0]}/{user}/envs/test

export MKL_SERVICE_FORCE_INTEL=1
python /home/{user[0]}/{user}/codespace/ML4IM/code/yolov7_custom/train.py --data /scratch/tmp/{user}/data/datasets/{dataset}/data.yaml --device 0,1,2,3 --project /scratch/tmp/{user}/data/results/{project_name} --name {index} --four-channels"""
    
def main():
    parser = argparse.ArgumentParser(description="Generate CPU and GPU scripts")
    parser.add_argument("--script_location", required=True, help="GPU script output name")
    parser.add_argument("--gpu_dataset", required=True, help="GPU script dataset name")
    parser.add_argument("--project_name", required=True, help ="Name of the project")
    parser.add_argument("--index",required=True, help="Index of split")
    args = parser.parse_args()

    gpu_script_content = build_gpu_script(args.gpu_dataset,args.index,args.project_name)
    os.makedirs(f"../sbatch/train/{args.project_name}", exist_ok=True)
    write_file(args.script_location,gpu_script_content)

if __name__ == "__main__":
    main()
