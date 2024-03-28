#!/bin/bash

id=$(sbatch cpu_o-bs-tf_hsv.sh | { read text; echo ${text##* };})
sbatch --dependency=afterok:$id gpu_o-bs-tf_hsv.sh

id=$(sbatch cpu_original_bg-sub_original_hsv.sh | { read text; echo ${text##* };})
sbatch --dependency=afterok:$id gpu_original_bg-sub_original_hsv.sh

id=$(sbatch cpu_original_bg-sub_temp-filter_hsv.sh | { read text; echo ${text##* };})
sbatch --dependency=afterok:$id gpu_original_bg-sub_temp-filter_hsv.sh

id=$(sbatch cpu_original_hsv.sh | { read text; echo ${text##* };})
sbatch --dependency=afterok:$id gpu_original_hsv.sh
 
id=$(sbatch cpu_o-tf-o_hsv.sh | { read text; echo ${text##* };})
sbatch --dependency=afterok:$id gpu_o-tf-o_hsv.sh
