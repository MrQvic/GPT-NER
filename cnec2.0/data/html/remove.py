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

def clean_html(html_content):
    """
    Clean HTML by removing non-name related span tags while preserving their content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # First pass: identify spans to remove
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
    input_file = "example.html"
    output_file = "cleaned_example.html"
    process_file(input_file, output_file)