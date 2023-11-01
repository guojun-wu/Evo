#!/bin/bash

#SBATCH --job-name=evo_comet
#SBATCH --time=00:00:30
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1

#SBATCH --account=ec255

srun /work/ec255/ec255/guojun/Evo/run_comet.sh