import json
import sys

def renumber_qas_ids(input_file, output_file):
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
    
    # Renumber qas_ids
    for i, record in enumerate(data):
        record["qas_id"] = f"{i}.1"
    
    # Write the renumbered data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        if isinstance(data, list) and first_char == '[':
            # Write as JSON array if input was an array
            json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            # Write as JSON objects one per line
            for record in data:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"Processed and renumbered {len(data)} records")
    print(f"Saved to {output_file}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python renumber_qas_ids.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if renumber_qas_ids(input_file, output_file):
        print("Renumbering completed successfully.")
    else:
        print("Renumbering failed.")