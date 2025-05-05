import json
import sys

def remove_long_contexts(input_file, output_file, max_words=30):
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
    
    # Filter records
    filtered_records = []
    removed_count = 0
    
    for record in data:
        context = record.get("context", "")
        # Count words in context
        word_count = len(context.split())
        
        if word_count <= max_words:
            filtered_records.append(record)
        else:
            removed_count += 1
    
    # Write the filtered data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        if isinstance(data, list) and first_char == '[':
            # Write as JSON array if input was an array
            json.dump(filtered_records, f, ensure_ascii=False, indent=2)
        else:
            # Write as JSON objects one per line
            for record in filtered_records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"Processed {len(data)} records")
    print(f"Removed {removed_count} records with context longer than {max_words} words")
    print(f"Saved {len(filtered_records)} records to {output_file}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_long_contexts.py <input_file> <output_file> [max_words]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Optional parameter for maximum word count
    max_words = 30
    if len(sys.argv) > 3:
        try:
            max_words = int(sys.argv[3])
        except ValueError:
            print(f"Warning: Invalid max_words value '{sys.argv[3]}'. Using default: 30")
    
    if remove_long_contexts(input_file, output_file, max_words):
        print("Filtering completed successfully.")
    else:
        print("Filtering failed.")