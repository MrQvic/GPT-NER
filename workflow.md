Embeddings are created using extract_mrc_knn.py for both random and sentence level.
Get llm predictions using either run_predictions.ps1 (powershell) or for ollama run_predictions.sh (bash)
Results are stored in filename specified in script in gpt3-data/conll_mrc/100-results folder
optional - run self-verification using run_verification.ps1 (powershell) 
Calculate recall, precision and f1 using run_evalutation.ps1

NOTE:   self-verification needs to be fixed for ollama
        when choosing openai model in get_results_mrc_knn, if you want to use older instruct model, you need to change the stlye of api call in base_access.py
        this repo needs complete refactoring and half of the code can be deleted