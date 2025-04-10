#!/bin/bash

REF="/home/xmrkva04/GPT-NER/gpt3-data/historical_ner_dataset/merged_annotations_1.json"
PRE="/home/xmrkva04/GPT-NER/gpt3-data/historical_ner_dataset/annotators_results/merged_annotations_1_robeczech_eval.txt"
python3 ../compute_f1.py \
    --candidate-file "$PRE" \
    --reference-file "$REF"