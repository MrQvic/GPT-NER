#!/bin/bash

SOURCEDIR="../../gpt3-data/conll_mrc/"
SOURCENAME="test.100"
DATANAME="CONLL"
EXAMPLEDIR="../../gpt3-data/conll_mrc/"
EXAMPLENAME="test.100.simcse.32"
EXAMPLENUM=8
WRITEDIR="../../gpt3-data/conll_mrc/100-results"
WRITENAME="qwen2.5-14b.100.sentence.level.test" 
TRAINNAME="train.dev"

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