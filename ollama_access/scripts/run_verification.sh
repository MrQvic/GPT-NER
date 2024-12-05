#!/bin/bash

MRCDIR="../../gpt3-data/conll_mrc/"
MRCNAME="test.100"
GPTDIR="../../gpt3-data/conll_mrc/100-results/"
GPTNAME="ollama.100.random.test"  # This should be your results file from previous step
DATANAME="CONLL"
WRITEDIR="../../gpt3-data/conll_mrc/100-results"
WRITENAME="ollama.100.random.verified"

/usr/bin/python3 ../verify_results.py \
    --mrc-dir "$MRCDIR" \
    --mrc-name "$MRCNAME" \
    --gpt-dir "$GPTDIR" \
    --gpt-name "$GPTNAME" \
    --data-name "$DATANAME" \
    --write-dir "$WRITEDIR" \
    --write-name "$WRITENAME"