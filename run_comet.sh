#!/bin/bash

set -e
source /work/ec255/ec255/guojun/evo/bin/activate

python main.py\
    --metric 'comet' \
    --data_path evo_data \
    --output_path result \
    --test \
