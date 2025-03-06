import requests
import json
import os
import re
from flask import jsonify ,flash
from searchbooks import  get_volume_id

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
    """Sends a description of a book and asks DeepSeek for similar books along with reasoning."""

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
                {"role": "system", "content": 
                    """You are a book recommendation assistant. Provide only the most direct and concise answer in JSON format.
                    
                    EXAMPLE INPUT:
                    List 6 books similar to '{book_title}' based on this description: '{book_description}'. 
                    For each book, provide a short reason (max 4 sentences) explaining why it's a good recommendation.

                    EXAMPLE JSON OUTPUT: 
                   {
                        "Recommendations": [
                            {
                                "title": "Harry Potter",
                                "reason": "Harry Potter is a coming-of-age fantasy novel with a strong hero's journey, much like {book_title}. 
                                           It features magic, adventure, and deep character development, making it appealing to fans of {book_title}. 
                                           Both stories explore themes of friendship and courage. Additionally, it has a vast world-building aspect similar to {book_title}."
                            },
                            {
                                "title": "Percy Jackson",
                                "reason": "Percy Jackson shares a young hero navigating supernatural challenges, much like {book_title}. 
                                           It has a fast-paced narrative and deep mythology that would appeal to fans of {book_title}."
                            }
                        ]
                   }
                    """},
                {"role": "user", "content": 
                    f"List 6 books similar to '{book_title}' based on this description: '{book_description}'. "
                    "For each book, provide a short reason (max 4 sentences) explaining why it's a good recommendation. "
                    "Return the result as a JSON object with a key 'Recommendations' containing a list of objects."
                }
            ],
            "top_p": 1,
            "temperature": 0.6,
            "max_tokens": 1500,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
            "response_format": {'type': 'json_object'}
        })
    )
    
    response.raise_for_status()

    try:
        ai_response = response.json()
        raw_content = ai_response["choices"][0]["message"]["content"]

        # Extract JSON content from triple backticks
        match = re.search(r'```json\s*(.*?)\s*```', raw_content, re.DOTALL)
        json_str = match.group(1) if match else raw_content  

        final_data = json.loads(json_str)  # Convert to Python dictionary

    except Exception as e:
        return {"error": f"Failed to parse AI response. Raw response: {response.text}. Error: {str(e)}"}

    # flash(f"AI Recommendations: {final_data}", "info")

    return final_data 

def similar_descript_ai(user_description):
    """Sends a User's description of a book and asks DeepSeek for similar books along with reasoning."""

    
    response = requests.post(
        url=OPRO_DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {OPRO_DEEPSEEK_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",  
            "messages": [
                {"role": "system", "content": 
                    """You are a book recommendation assistant. Provide only the most direct and concise answer in JSON format.
                    
                    INSTRUCTION:
                    List 6 books similar  based on this description: '{user_description}'. 
                    For each book, provide a short reason (max 4 sentences) explaining why it's a good recommendation.

                    EXAMPLE INPUT:
                    "I'm looking for a book about a young hero who discovers a hidden magical world and must battle dark forces."  


                    EXAMPLE JSON OUTPUT: 
                   {
                        "Recommendations": [
                            {
                                "title": "Harry Potter",
                                "reason": "This novel follows a young hero, Harry, as he discovers the hidden magical world of Hogwarts. 
                                    It blends adventure, friendship, and the battle between good and evil, perfectly matching your description."
                            },
                            {
                                "title": "Percy Jackson",
                                "reason": "Percy, like your hero, is thrust into a hidden world—Greek mythology come to life. 
                                    The fast-paced narrative, humor, and rich mythological elements make it an exciting and immersive read."
                            }
                        ]
                   }
                    """},
                {"role": "user", "content": 
                    f"List 6 books similar based on this description: '{user_description}'. "
                    "For each book, provide a short reason (max 4 sentences) explaining why it's a good recommendation. "
                    "Return the result as a JSON object with a key 'Recommendations' containing a list of objects."
                }
            ],
            "top_p": 1,
            "temperature": 0.6,
            "max_tokens": 1500,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
            "response_format": {'type': 'json_object'}
        })
    )
    
    response.raise_for_status()

    try:
        ai_response = response.json()
        raw_content = ai_response["choices"][0]["message"]["content"]

        # Extract JSON content from triple backticks
        match = re.search(r'```json\s*(.*?)\s*```', raw_content, re.DOTALL)
        json_str = match.group(1) if match else raw_content  

        final_data = json.loads(json_str)  # Convert to Python dictionary

    except Exception as e:
        return {"error": f"Failed to parse AI response. Raw response: {response.text}. Error: {str(e)}"}


    return final_data 
