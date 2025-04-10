import json
import argparse
from collections import defaultdict

# Function to find duplicate contexts in JSON file
# Function reads JSON file and groups records by 'context' value

def find_duplicate_contexts(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Chyba: Soubor {json_file} není platný JSON.")
        return {}
    except Exception as e:
        print(f"Chyba při čtení souboru {json_file}: {str(e)}")
        return {}
    
    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
    
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                records = value
                break
    
    if not records:
        print(f"V souboru {json_file} nebyl nalezen žádný seznam záznamů.")
        return {}
    
    # Seskupíme záznamy podle hodnoty 'context'
    context_groups = defaultdict(list)
    for record in records:
        if isinstance(record, dict) and 'context' in record:
            context = record['context']
            context_groups[context].append(record)
    
    # Vrátíme pouze skupiny, které mají víc než jeden záznam
    return {context: records for context, records in context_groups.items() if len(records) > 2}

# Function to print duplicate info
# Function prints information about duplicate groups

def print_duplicate_info(duplicate_groups):
    if not duplicate_groups:
        print("Žádné duplicitní záznamy nebyly nalezeny.")
        return
    
    print(f"\nNalezeno {len(duplicate_groups)} duplicitních hodnot 'context':")
    
    total_duplicates = 0
    for i, (context, records) in enumerate(duplicate_groups.items(), 1):
        duplicates_count = len(records) - 1
        total_duplicates += duplicates_count

        #if duplicates_count < 2:
        #    continue
        
        print(f"\n{i}. Duplicitní 'context' (celkem {len(records)} záznamů):")
        print(f"   \"{context[:100]}{'...' if len(context) > 100 else ''}\"")
        
        print("\n   Detaily záznamů:")
        for j, record in enumerate(records, 1):
            qas_id = record.get('qas_id', 'N/A')
            entity_label = record.get('entity_label', 'N/A')
            
            # Check if span_position list is empty
            span_list = record.get('span_position', [])
            span = span_list[0] if span_list else 'N/A'

            id = record.get('anotator_id', 'N/A')
            
            # Check if this record has any person annotations
            is_impossible = record.get('impossible', False)
            annotation_status = "No annotations" if is_impossible else f"Span: {span}"
            
            print(f"   {j}. ID: {qas_id}, Entity: {entity_label}, {annotation_status}, Anotator ID: {id}")
    
    print(f"\nCelkem nalezeno {total_duplicates} duplicitních záznamů v {len(duplicate_groups)} skupinách.")

# Main function
# Function to parse arguments and run the script

def main():
    parser = argparse.ArgumentParser(description='Najde duplicitní záznamy v JSON souboru podle pole "context".')
    parser.add_argument('json_file', help='Cesta k JSON souboru')
    parser.add_argument('--output', '-o', help='Uložit výsledky do JSON souboru')
    args = parser.parse_args()
    
    print(f"Hledání duplicitních záznamů v souboru: {args.json_file}")
    
    duplicate_groups = find_duplicate_contexts(args.json_file)
    print_duplicate_info(duplicate_groups)
    
    #if args.output and duplicate_groups:
    #    try:
    #        with open(args.output, 'w', encoding='utf-8') as f:
    #            json.dump(duplicate_groups, f, ensure_ascii=False, indent=2)
    #        print(f"\nVýsledky byly uloženy do souboru: {args.output}")
    #    except Exception as e:
    #        print(f"Chyba při ukládání výsledků: {str(e)}")


if __name__ == "__main__":
    main()