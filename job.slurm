#!/bin/bash

#SBATCH --job-name=evo_comet
#SBATCH --time=00:15:00
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --account=ec255
#SBATCH --output=job.out

cd /work/ec255/ec255/guojun/Evo


module load python/3.9.13
source /work/ec255/ec255/guojun/evo/bin/activate

srun ./run_comet.sh