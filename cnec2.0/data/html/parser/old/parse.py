from bs4 import BeautifulSoup
import re
import json

def get_word_positions(text):
    positions = {}  # {word: [positions in order]}
    word_counts = {}  # Track current count of each word
    words = text.split()
    
    # Store each word's positions in order
    for i, word in enumerate(words):
        if word not in positions:
            positions[word] = []
            word_counts[word] = 0
        positions[word].append(i)
        word_counts[word] += 1
            
    return positions, words, word_counts

def get_positions(soup):
    clean_text = ' '.join(soup.get_text().split())
    word_pos, words, word_counts = get_word_positions(clean_text)
    
    word_indices = {}  # Track current index for each word
    for word in word_counts:
        word_indices[word] = 0

    positions = []
        
    for span in soup.find_all('span'):
        if span.name == 'span':
            span_text = span.get_text()
            span_words = span_text.split()
            
            try:
                if len(span_words) > 1:
                    first_word = span_words[0]
                    last_word = span_words[-1]
                    
                    # Check if words exist and haven't exceeded their counts
                    if (first_word in word_pos and last_word in word_pos and 
                        word_indices[first_word] < len(word_pos[first_word]) and
                        word_indices[last_word] < len(word_pos[last_word])):
                        
                        start_pos = word_pos[first_word][word_indices[first_word]]
                        end_pos = word_pos[last_word][word_indices[last_word]]
                        word_indices[first_word] += 1
                        word_indices[last_word] += 1
                        positions.append((start_pos, end_pos))
                else:
                    word = span_text
                    if word in word_pos and word_indices[word] < len(word_pos[word]):
                        pos = word_pos[word][word_indices[word]]
                        word_indices[word] += 1
                        positions.append((pos, pos))
            except Exception as e:
                print(f"Error processing span '{span_text}': {str(e)}")
                continue

    return positions

def process_line(line, qas_id):
    """
    Process a single line and create entries for person entities.
    """
    soup = BeautifulSoup(line, 'html.parser')

    # Get clean text (without HTML tags)
    clean_text = ' '.join(soup.get_text().split())

    if not clean_text:
        return None

    # Get positions of person entities
    positions = get_positions(soup)
    
    # Create entry for impossible case (when no persons found)
    impossible_entry = {
        "context": clean_text,
        "end_position": [],
        "entity_label": "PER",
        "impossible": "true",
        "qas_id": f"{qas_id}.1",
        "query": "person entities are named persons or family.",
        "span_position": [],
        "start_position": []
    }
    
    # If we found person entities, update the positions
    if positions:
        impossible_entry["impossible"] = "false"
        impossible_entry["start_position"] = [pos[0] for pos in positions]
        impossible_entry["end_position"] = [pos[1] for pos in positions]
        impossible_entry["span_position"] = [f"{pos[0]};{pos[1]}" for pos in positions]
    
    return impossible_entry

def parse_html_lines(html_content):
    """
    Parse HTML content and extract lines that end with .<br/>
    """
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get the content
    content = str(soup)
    
    # Split by <br/> tags
    # Using regex to handle potential spacing variations in <br/> tag
    lines = re.split(r'<br\s*?/>', content)
    
    # Process each line
    id = 0
    results = []
    for line in lines:
        if line.strip() == '':
            continue
        print(line)
        json_entry = process_line(line, id)
        if json_entry:
            results.append(json_entry)
            id += 1
    return results

def process_file(file_path, output_path):
    """
    Read and process an HTML file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        results = parse_html_lines(content)
        # Save results
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "cleaned_dtest.html"
    output_path = "parsed.dtest"
    process_file(input_file, output_path)