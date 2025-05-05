import json
import os

def sort_entries_by_annotator(input_file, output_dir="annotator_files"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Dictionary to store entries by annotator
    annotator_entries = {}
    
    # Sort entries by annotator_id
    for entry in data:
        if 'anotator_id' in entry:
            annotator_id = entry['anotator_id']
            if annotator_id not in annotator_entries:
                annotator_entries[annotator_id] = []
            annotator_entries[annotator_id].append(entry)
    
    # Write separate files for each annotator
    for annotator_id, entries in annotator_entries.items():
        output_file = os.path.join(output_dir, f'annotator_{annotator_id}.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"Created file for annotator {annotator_id} with {len(entries)} entries")

if __name__ == "__main__":
    input_file = "Historical-NER-Dataset_gpt_ner_fmt_FULL_42.json"
    sort_entries_by_annotator(input_file)