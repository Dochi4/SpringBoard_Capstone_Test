import requests
import json
import os


OPRO_DEEPSEEK_KEY = os.environ.get("OPRO_DEEPSEEK_KEY")
OPRO_DEEPSEEK_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_ai(content):
    """Send a request to DeepSeek AI and return the response."""
    response = requests.post(
        url=OPRO_DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {OPRO_DEEPSEEK_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free", 
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Provide only the most direct and concise answer without explanations or thinking process." },
                {"role": "user","content": f"{content}"}
                ],
            "top_p": 1,
            "temperature": 0.3,
            "max_tokens": 500,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
        })
    )
    response.raise_for_status()
        
    return response.json()

def similar_book_ai(book):
    """Sends a description of a book and asks DeepSeek for similar books."""
    book_title = book.get('title', 'Untitled')
    book_description = book.get('description', 'No description available')

    response = requests.post(
        url=OPRO_DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {OPRO_DEEPSEEK_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",  
            "messages": [
                {"role": "system", "content": "You are a book recommendation assistant. Provide only the most direct and concise answer as a JSON list."},
                {"role": "user", "content": f"List 10 books similar to '{book_title}' based on this description: '{book_description}'. Return the result as a JSON list."}
            ],
            "top_p": 1,
            "temperature": 0.3,
            "max_tokens": 500,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
        })
    )
    
    response.raise_for_status()
    
    return response.json()
