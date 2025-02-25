REF="/home/xmrkva04/GPT-NER/gpt3-data/cnec_mrc/mrc-ner.test.100"
PRE="/home/xmrkva04/GPT-NER/gpt3-data/cnec_mrc/100-results/marked_contexts.txt"
python3 ../compute_f1.py \
    --candidate-file "$PRE" \
    --reference-file "$REF"