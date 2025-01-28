REF="/home/xmrkva04/GPT-NER/gpt3-data/cnec_mrc/mrc-ner.test.100"
PRE="/home/xmrkva04/GPT-NER/gpt3-data/cnec_mrc/100-results/qwen2.5-72b.train.100.random.level.test"
python ../compute_f1.py \
    --candidate-file "$PRE" \
    --reference-file "$REF"