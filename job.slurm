#!/bin/bash

#SBATCH --job-name=evo_comet
#SBATCH --time=10:00:00
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --account=ec255
#SBATCH --output=job.out

export TRANSFORMERS_CACHE=/work/ec255/ec255/guojun/.cache/huggingface/hub
export MPLCONFIGDIR=/work/ec255/ec255/guojun/.config/matplotlib
cd /work/ec255/ec255/guojun/Evo

module load nvidia/nvhpc/22.2
source /work/ec255/ec255/guojun/evo/bin/activate

srun ./run_comet.sh