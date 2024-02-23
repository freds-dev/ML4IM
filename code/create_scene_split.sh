#!/bin/bash

echo "Build a datset for project $1 and scene $2"
    python utils/build_split_script.py --project_name $1 --scene_name $2 --video_event_name $3 --video_rgb_name $4 --config_name $5
if [ "$6" -eq -1 ]; then
    echo "No dependency"
    id=$(sbatch sbatch/pp/$1/$2.sh| { read text; echo ${text##* };})
else
    echo "Dependency: $6"
    id=$(sbatch --dependency=afterok:$6 sbatch/pp/$1/$2.sh| { read text; echo ${text##* };})
fi
echo "Submitted preprocessing for $i split on id: $id"
python utils/build_sbatch.py --script_location sbatch/train/$1/$2.sh --gpu_dataset $1.$2 --index $2 --project_name $1
sbatch --dependency=afterok:$id sbatch/train/$1/$2.sh
echo "\n\n\n"
echo $id

