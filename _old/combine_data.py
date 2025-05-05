import json

# Read train file
with open('./gpt3-data/conll_mrc/mrc-ner.train', 'r', encoding='utf-8') as f:
    train_data = json.load(f)

# Read dev file
with open('./gpt3-data/conll_mrc/mrc-ner.dev', 'r', encoding='utf-8') as f:
    dev_data = json.load(f)

# Combine them
combined_data = train_data + dev_data

# Write combined file
with open('./gpt3-data/conll_mrc/mrc-ner.train.dev', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)

print(f"Number of examples in train: {len(train_data)}")
print(f"Number of examples in dev: {len(dev_data)}")
print(f"Number of examples in combined: {len(combined_data)}")