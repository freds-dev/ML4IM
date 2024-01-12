import argparse
from helper import adjust_string_length, whoami
import os

def write_file(path,content):
    # If dir is not exisitng just create it:
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    f = open(path, "w")
    f.write(content)
    f.close()
    print(f"Saved content to {path}")

def build_split_script(project_name,scene_name, amount_cpus=18, memory=48, hours=1, partition="normal"):
    user = whoami()
    return f"""#!/bin/bash

#SBATCH --job-name=pp-split-{project_name}{scene_name}
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={amount_cpus}
#SBATCH --mem={memory}G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition={partition}          # on which partition to submit the job
#SBATCH --time={hours}:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/{project_name}/pp/{scene_name}.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user={user}@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/{user[0]}/{user}/envs/test

python /home/{user[0]}/{user}/codespace/ML4IM/code/split_dataset.py -video_dir_name {project_name} -dataset {project_name}.{scene_name} -scene {scene_name}"""

def main():
    parser = argparse.ArgumentParser(description="Build a split script")
    parser.add_argument("--project_name", type=str, required=True, help="Name of the project: The name of the used dataset")
    parser.add_argument("--scene_name", type=str, required=True, help="Name of the scen")
    parser.add_argument("--cpus", type=int, default=18, help="Number of CPUs")
    parser.add_argument("--memory", type=int, default=48, help="Memory in GB")
    parser.add_argument("--hours", type=int, default=1, help="Wallclock time in hours")
    parser.add_argument("--partition", default="normal", help="Partition for the job")

    args = parser.parse_args()

    split_script = build_split_script(args.project_name,args.scene_name, args.cpus, args.memory, args.hours, args.partition)
    os.makedirs(f"sbatch/pp/{args.project_name}", exist_ok=True)
    with open(f"sbatch/pp/{args.project_name}/{args.scene_name}.sh", "w") as script_file:
        script_file.write(split_script)

if __name__ == "__main__":
    main()
