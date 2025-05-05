# Define variables
$MRCDIR = "..\..\gpt3-data\cnec_mrc\"
$MRCNAME = "test.100"
$GPTDIR = "..\..\gpt3-data\cnec_mrc\100-results\"
$GPTNAME = "qwen2.5-72b.train.100.random.level.test"  # This should be your results file from previous step
$DATANAME = "CNEC"
$WRITEDIR = "..\..\gpt3-data\conll_mrc\100-results"
$WRITENAME = "ollama.100.random.verified"

# Execute Python script with parameters
python ..\verify_results.py `
    --mrc-dir $MRCDIR `
    --mrc-name $MRCNAME `
    --gpt-dir $GPTDIR `
    --gpt-name $GPTNAME `
    --data-name $DATANAME `
    --write-dir $WRITEDIR `
    --write-name $WRITENAME