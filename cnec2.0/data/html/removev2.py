from bs4 import BeautifulSoup, Tag
import re

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

def process_file(input_path, output_path):
    """
    Process an HTML file and write the cleaned version to a new file.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        cleaned_content = clean_html(content)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
            
        print(f"Successfully processed {input_path} and saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "named_ent_dtest.html"
    output_file = "cleaned_dtest.html"
    process_file(input_file, output_file)