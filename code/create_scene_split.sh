#!/bin/bash

echo "Build a datset for project $1 and scene $2"
python utils/build_split_script.py --project_name $1 --scene_name $2
id=$(sbatch sbatch/pp/$1/$2.sh| { read text; echo ${text##* };})
echo "Submitted preprocessing for $i split on id: $id"
python utils/build_sbatch.py --script_location sbatch/train/$1/$2.sh --gpu_dataset $1.$2 --index $2 --project_name $1
sbatch --dependency=afterok:$id sbatch/train/$1/$2.sh

