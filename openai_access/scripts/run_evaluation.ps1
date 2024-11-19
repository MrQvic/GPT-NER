$REF = ".\gpt3-data\conll_mrc\mrc-ner.test.100"
$PRE = ".\gpt3-data\conll_mrc\100-results\tmp.test.verified"

python openai_access/compute_f1.py `
    --candidate-file $PRE `
    --reference-file $REF