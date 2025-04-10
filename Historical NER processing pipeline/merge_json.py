import json
import os
import argparse

def merge_json_files(file1, file2, output_file):
    """
    Merge two JSON annotation files into a single file.
    
    Args:
        file1 (str): Path to the first JSON file
        file2 (str): Path to the second JSON file
        output_file (str): Path for the output merged file
    """
    # Read the first file
    with open(file1, 'r', encoding='utf-8') as f1:
        data1 = json.load(f1)
    
    # Read the second file
    with open(file2, 'r', encoding='utf-8') as f2:
        data2 = json.load(f2)
    
    # Combine the data
    merged_data = data1 + data2
    
    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, indent=2)
    
    print(f"Successfully merged {len(data1)} items from {os.path.basename(file1)} and {len(data2)} items from {os.path.basename(file2)}")
    print(f"Total {len(merged_data)} items written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge two JSON annotation files')
    parser.add_argument('file1', help='Path to the first JSON file')
    parser.add_argument('file2', help='Path to the second JSON file')
    parser.add_argument('--output', '-o', default='merged_annotations.json', 
                        help='Output file path (default: merged_annotations.json)')
    
    args = parser.parse_args()
    
    merge_json_files(args.file1, args.file2, args.output)