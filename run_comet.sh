#!/bin/bash

set -e
source /work/ec255/ec255/guojun/evo/bin/activate

export BASE_DIR=/work/ec255/ec255/guojun/Evo
python $BASE_DIR/main.py\
    --metric 'comet' \
    --data_path $BASE_DIR/evo_data \
    --output_path $BASE_DIR/result \
    --test >> $BASE_DIR/log_file.log 2>&1 &

echo "Script has started at $(date)" >> $BASE_DIR/log_file.log
