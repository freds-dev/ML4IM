import argparse
from helper import adjust_string_length

def build_split_script(index, amount_cpus=18, memory=48, hours=1, partition="normal"):
    return f"""#!/bin/bash

#SBATCH --job-name=pp-split-{adjust_string_length(str(index), 3, '0')}
#SBATCH --export=NONE               # Start with a clean environment
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={amount_cpus}
#SBATCH --mem={memory}G                   # how much memory is needed per node (units can be: K, M, G, T)
#SBATCH --partition={partition}          # on which partition to submit the job
#SBATCH --time={hours}:00:00             # the max wallclock time (time limit your job will run)
#SBATCH --output=logs/pp-split-{adjust_string_length(str(index), 3, '0')}.dat         # the file where output is written to (stdout & stderr)
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=jdanel@uni-muenster.de # your mail address
#SBATCH --nice=100
 
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/j/jdanel/envs/test

python split_dataset.py -video_dir_name original -dataset split_{adjust_string_length(str(index), 3, '0')} -index {index}
"""

def main():
    parser = argparse.ArgumentParser(description="Build a split script")
    parser.add_argument("--index", type=int, required=True, help="Index for the split script")
    parser.add_argument("--cpus", type=int, default=18, help="Number of CPUs")
    parser.add_argument("--memory", type=int, default=48, help="Memory in GB")
    parser.add_argument("--hours", type=int, default=1, help="Wallclock time in hours")
    parser.add_argument("--partition", default="normal", help="Partition for the job")

    args = parser.parse_args()

    split_script = build_split_script(args.index, args.cpus, args.memory, args.hours, args.partition)

    with open(f"../cpu_split_script_{adjust_string_length(str(args.index), 3, '0')}.sh", "w") as script_file:
        script_file.write(split_script)

if __name__ == "__main__":
    main()
