# First verification
$MRCDIR = ".\gpt3-data\conll_mrc\"
$MRCNAME = "test.100"
$GPTDIR = ".\gpt3-data\conll_mrc\100-results\"
$GPTNAME = "tmp.test"
$DATANAME = "CONLL"
$WRITEDIR = ".\gpt3-data\conll_mrc\100-results"
$WRITENAME = "tmp.test.verified"

python openai_access/verify_results.py `
    --mrc-dir $MRCDIR `
    --mrc-name $MRCNAME `
    --gpt-dir $GPTDIR `
    --gpt-name $GPTNAME `
    --data-name $DATANAME `
    --write-dir $WRITEDIR `
    --write-name $WRITENAME

# Then evaluation
python openai_access/compute_f1.py `
    --candidate-file ".\gpt3-data\conll_mrc\100-results\tmp.test.verified" `
    --reference-file ".\gpt3-data\conll_mrc\mrc-ner.test.100"