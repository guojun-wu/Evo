#!/bin/bash

#SBATCH --job-name=evo
#SBATCH --time=00:10:00
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --account=ec255
#SBATCH --output=job.out

export TRANSFORMERS_CACHE=/work/ec255/ec255/guojun/.cache/huggingface/hub
export MPLCONFIGDIR=/work/ec255/ec255/guojun/.config/matplotlib
cd /work/ec255/ec255/guojun/Evo

module load nvidia/nvhpc/22.2
source /home/ec255/ec255/guojun/.bashrc
conda activate evo

srun ./run_comet.sh