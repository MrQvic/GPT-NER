

$REF = "..\..\gpt3-data\historical_ner_dataset\mrc-ner.SDMA_test_qid_sorted.json"
$PRE = "..\..\gpt3-data\historical_ner_dataset\114-results\qwen2.5-72b.test.114.random.level.test.verified"
python ..\compute_f1.py `
    --candidate-file $PRE `
    --reference-file $REF