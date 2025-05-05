from bs4 import BeautifulSoup, Tag
import re
import json

def should_keep_span(tag):
    """
    Determine if a span tag should be kept based on its class.
    Keep spans that are related to person names (namedent_p or namedent_P).
    """
    if not isinstance(tag, Tag):
        return False
    
    if tag.name != 'span':
        return True
        
    classes = tag.get('class', [])
    if not classes:
        return False
        
    # Keep spans with person-related classes
    return any(cls.startswith('namedent_p') or cls.startswith('namedent_P') for cls in classes)

def process_namedent_P(span):
    """
    Process a namedent_P span by combining all internal spans into one text.
    """
    # Get all text content, stripping whitespace but preserving spaces between parts
    texts = []
    for content in span.contents:
        if isinstance(content, Tag):
            texts.append(content.get_text().strip())
        else:
            # For non-tag content (like spaces), preserve only if it's not empty
            text = content
            if text:
                texts.append(text)
    
    # Create new span with combined text
    new_span = Tag(name='span')
    new_span['class'] = span['class']
    new_span.string = ''.join(texts)
    return new_span

def clean_html(html_content):
    """
    Clean HTML by removing non-name related span tags while preserving their content.
    Also combines internal spans within namedent_P spans.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # First process namedent_P spans
    for span in soup.find_all('span', class_='namedent_P'):
        new_span = process_namedent_P(span)
        span.replace_with(new_span)
    
    # Then process remaining spans
    spans_to_process = soup.find_all('span')
    for span in spans_to_process:
        if not should_keep_span(span):
            # Replace span with its contents
            span.unwrap()
    
    return str(soup)

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
        "impossible": True if not positions else False,
        "qas_id": f"{qas_id}.1",
        "query": "person entities are named persons or family.",
        "span_position": [],
        "start_position": []
    }
    
    # If we found person entities, update the positions
    if positions:
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
    lines = re.split(r'<br\s*?/>', content)
    
    # Process each line
    id = 0
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        json_entry = process_line(line, id)
        if json_entry:
            results.append(json_entry)
            id += 1
    
    return results

def process_file(input_path, output_path, cleaned_path=None):
    """
    Process an HTML file containing named entities to extract persons
    and convert to JSON format compatible with GPT-NER.
    
    Args:
        input_path: Path to the input HTML file
        output_path: Path to save the output JSON file
        cleaned_path: Optional path to save the cleaned HTML file
    """
    try:
        # Read the input file
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Clean the HTML by keeping only person-related spans
        cleaned_content = clean_html(content)
        
        # Optionally save the cleaned HTML
        if cleaned_path:
            with open(cleaned_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Saved cleaned HTML to {cleaned_path}")
        
        # Parse the cleaned HTML and extract person entities
        results = parse_html_lines(cleaned_content)
        
        # Save the results as JSON
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
        
        print(f"Successfully processed {input_path} and saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process HTML files with named entities and convert to GPT-NER compatible JSON')
    parser.add_argument('input_file', help='Path to the input HTML file')
    parser.add_argument('output_file', help='Path to save the output JSON file')
    parser.add_argument('--save-cleaned', help='Path to save the cleaned HTML file (optional)', default=None)
    
    args = parser.parse_args()
    
    process_file(args.input_file, args.output_file, args.save_cleaned)