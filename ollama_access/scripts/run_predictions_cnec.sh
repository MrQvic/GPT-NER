#!/bin/bash

SOURCEDIR="../../gpt3-data/cnec_mrc/"
SOURCENAME="test.100"
DATANAME="CNEC"
EXAMPLEDIR="../../gpt3-data/cnec_mrc/"
EXAMPLENAME="test.100.cnec.random.8"
EXAMPLENUM=8
WRITEDIR="../../gpt3-data/cenc_mrc/100-results"
WRITENAME="qwen2.5-72b.train.100.random.level.test" 
TRAINNAME="train"

/usr/bin/python3 ../get_results_mrc_knn.py \
    --source-dir "$SOURCEDIR" \
    --source-name "$SOURCENAME" \
    --data-name "$DATANAME" \
    --example-dir "$EXAMPLEDIR" \
    --example-name "$EXAMPLENAME" \
    --example-num "$EXAMPLENUM" \
    --train-name "$TRAINNAME" \
    --write-dir "$WRITEDIR" \
    --write-name "$WRITENAME"