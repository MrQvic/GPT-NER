import json
with open('./gpt3-data/conll_mrc/mrc-ner.train.dev') as f:
    train_data = json.load(f)
print(f"Number of train+dev examples: {len(train_data)}")