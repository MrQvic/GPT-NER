import json
import os
from collections import defaultdict

def organize_by_annotator(input_file, output_dir="annotator_files", target_annotators=["01", "02", "03"]):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for only annotations from annotators 1, 2, and 3
    filtered_data = [entry for entry in data if 'anotator_id' in entry and entry['anotator_id'] in target_annotators]
    
    # Step 1: Group entries by context
    contexts = defaultdict(list)
    for entry in filtered_data:
        if 'context' in entry:
            context_text = entry['context']
            contexts[context_text].append(entry)
    
    # Step 2: Find contexts annotated by all target annotators
    multi_annotated_contexts = {}
    for context, entries in contexts.items():
        annotator_ids = set(entry['anotator_id'] for entry in entries)
        if all(annotator_id in annotator_ids for annotator_id in target_annotators):
            multi_annotated_contexts[context] = entries
    
    # Step 3: Group entries by annotator_id
    annotator_entries = defaultdict(list)
    
    # Only include entries from contexts that have multiple annotators
    for context, entries in multi_annotated_contexts.items():
        for entry in entries:
            annotator_entries[entry['anotator_id']].append(entry)
    
    # Step 4: Write separate files for each annotator
    for annotator_id, entries in annotator_entries.items():
        output_file = os.path.join(output_dir, f'annotator_{annotator_id}.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"Created file for annotator {annotator_id} with {len(entries)} entries")
    
    # Print summary
    print(f"\nFound {len(multi_annotated_contexts)} contexts with multiple annotators from the target group")
    for annotator_id, entries in annotator_entries.items():
        print(f"Annotator {annotator_id}: {len(entries)} entries")

if __name__ == "__main__":
    input_file = "Historical-NER-Dataset_gpt_ner_fmt_FULL.json"
    organize_by_annotator(input_file, target_annotators=["01", "02", "03"])