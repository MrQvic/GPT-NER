import requests
import logging
from typing import List
import re

logger = logging.getLogger(__name__)

class AccessBase(object):
    def __init__(self, model, temperature=0.0, max_tokens=512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def get_multiple_sample(self, prompt_list: List[str]):
        results = []
        total = len(prompt_list)
        
        for i, prompt in enumerate(prompt_list, 1):
            print(f"Processing request {i}/{total}")
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens
                    }
                )
                response.raise_for_status()
                data = response.json()
                final_response = data.get("response", "")
		
                # Clean up response
                filtered = re.sub(r'<think>.*?</think>', '', final_response, flags=re.DOTALL)
                filtered = re.sub(r'\n{3,}', '\n\n', filtered)
                filtered = filtered.strip()
                
                # Remove newlines
                filtered = filtered.replace('\n', ' ') 
                    
                results.append(filtered)
            except Exception as e:
                logger.error(f"Error calling Ollama API: {str(e)}")
                results.append("")
        return results