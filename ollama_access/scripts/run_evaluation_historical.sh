#!/bin/bash

REF="/home/xmrkva04/GPT-NER/gpt3-data/historical_ner_dataset/mrc-ner.test.short.json"
PRE="/home/xmrkva04/GPT-NER/gpt3-data/historical_ner_dataset/154-results/qwen2.5-72b.test.short.random.level.test"
python3 ../compute_f1.py \
    --candidate-file "$PRE" \
    --reference-file "$REF"