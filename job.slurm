#!/bin/bash

#SBATCH --job-name=evo_comet
#SBATCH --time=00:20:00
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1

#SBATCH --account=ec255
cd /work/ec255/ec255/guojun/Evo

module load python/3.9.13

srun ./run_comet.sh