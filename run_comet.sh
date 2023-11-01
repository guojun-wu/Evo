#!/bin/bash

set -e
source /work/ec255/ec255/guojun/evo/bin/activate

export BASE_DIR=/work/ec255/ec255/guojun/Evo
python $BASE_DIR/main.py >> $BASE_DIR/log_file.log 2>&1 & \
    --metric=comet \
    --data_path=$BASE_DIR/evo_data \
    --output_path=$BASE_DIR/result \
    --test\

echo "Script has started at $(date)" >> $BASE_DIR/log_file.log
