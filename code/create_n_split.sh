#!/bin/bash

for i in {1..34}; do
    formatted_number=$(printf "%03d" $i)
    echo "Build a datset for: $formatted_number"
    python utils/build_split_script.py --index i
    id=$(sbatch cpu_split_script_$formatted_number.sh| { read text; echo ${text##* };})
    echo "Submitted preprocessing for $i split on id: $id"
    python utils/build_sbatch.py --script_location ../gpu_split_script_$formatted_number.sh --gpu_dataset split_$formatted_number --ndex $formatted_number
    sbatch --dependency=afterok:$id gpu_split_script$formatted_number.sh
done
