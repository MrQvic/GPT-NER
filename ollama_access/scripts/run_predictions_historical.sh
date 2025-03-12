#!/bin/bash

SOURCEDIR="../../gpt3-data/historical_ner_dataset/"
SOURCENAME="test.100.json"
DATANAME="HISTORICAL"
EXAMPLEDIR="../../gpt3-data/historical_ner_dataset/"
EXAMPLENAME="test.154.historical_ner_dataset.random.8"
EXAMPLENUM=8
WRITEDIR="../../gpt3-data/historical_ner_dataset/154-results"
WRITENAME="qwen2.5-72b.test.154.random.level.test" 
TRAINNAME="train.json"

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