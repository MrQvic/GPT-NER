REF="/home/xmrkva04/GPT-NER/gpt3-data/conll_mrc/mrc-ner.test.100"
PRE="/home/xmrkva04/GPT-NER/gpt3-data/conll_mrc/100-results/qwen2.5-14b.100.sentence.level.test"
python ../compute_f1.py \
    --candidate-file "$PRE" \
    --reference-file "$REF"