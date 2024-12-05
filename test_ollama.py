import requests

def generate_response(prompt, model="llama3.1"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

if __name__ == "__main__":
    result = generate_response("Why is the sky blue?")
    print(result)