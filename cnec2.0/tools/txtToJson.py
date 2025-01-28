import re
import json

def extract_names(text):
    """
    Extrahuje osobní jména z textu označená tagy <p nebo <P.
    Vrací seznam objektů ve formátu podobném výstupnímu JSONu.
    """
    # Regex pro nalezení osobních jmen (včetně víceslovných jmen)
    name_pattern = r'<[pP](?:[^>]*?)>([^<]+?)<'
    
    results = []
    qas_id_counter = 0
    
    # Rozdělíme text na věty (přibližně)
    sentences = text.split('.')
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Najdeme všechny osobní jména v této větě
        names = re.finditer(name_pattern, sentence)
        names_found = False
        
        for match in names:
            names_found = True
            name = match.group(1).strip()
            
            # Vytvoříme objekt podobný příkladu v output.txt
            result = {
                "context": sentence.strip(),
                "end_position": [len(name.split())],  # Aproximace pozice konce
                "entity_label": "PER",
                "impossible": False,
                "qas_id": f"{qas_id_counter}.1",
                "query": "person entities are named persons or family.",
                "span_position": [f"0;{len(name.split())-1}"],  # Aproximace span pozice
                "start_position": [0]
            }
            
            results.append(result)
            qas_id_counter += 1
            
        # Přidáme negative sample pokud ve větě nebylo žádné jméno
        if not names_found:
            result = {
                "context": sentence.strip(),
                "end_position": [],
                "entity_label": "PER",
                "impossible": True,
                "qas_id": f"{qas_id_counter}.1",
                "query": "person entities are named persons or family.",
                "span_position": [],
                "start_position": []
            }
            results.append(result)
            qas_id_counter += 1
    
    return results

def main():
    # Načteme vstupní soubor
    with open('example.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extrahujeme jména
    results = extract_names(text)
    
    # Zapíšeme výsledky do JSON souboru
    with open('parsed_names.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()