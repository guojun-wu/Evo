#!/bin/bash

#SBATCH --job-name=evo_comet
#SBATCH --time=00:20:00
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1

#SBATCH --account=ec255

srun run_comet.sh