import json
import sys
from collections import defaultdict

def remove_duplicates(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            # Check if file contains a JSON array
            first_char = f.read(1)
            f.seek(0)  # Reset file pointer
            
            if first_char == '[':
                # File contains a JSON array
                data = json.load(f)
            else:
                # File contains JSON objects one per line
                data = [json.loads(line) for line in f if line.strip()]
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in input file.")
            return False
    
    # Dictionary to track unique contexts
    unique_contexts = {}
    duplicates_count = 0
    
    # Process records
    unique_records = []
    for record in data:
        context = record.get("context")
        if context and context not in unique_contexts:
            unique_contexts[context] = True
            unique_records.append(record)
        else:
            duplicates_count += 1
    
    # Write the deduplicated data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        if isinstance(data, list) and first_char == '[':
            # Write as JSON array if input was an array
            json.dump(unique_records, f, ensure_ascii=False, indent=2)
        else:
            # Write as JSON objects one per line
            for record in unique_records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"Processed {len(data)} records")
    print(f"Removed {duplicates_count} duplicates")
    print(f"Saved {len(unique_records)} unique records to {output_file}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_duplicates.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if remove_duplicates(input_file, output_file):
        print("Deduplication completed successfully.")
    else:
        print("Deduplication failed.")