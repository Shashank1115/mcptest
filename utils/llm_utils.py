import os
import requests

GROQ_API_KEY="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"
GROQ_MODEL = "llama3-70b-8192"

def call_llm(prompt, model=GROQ_MODEL):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] LLM call failed: {e}")
        return ""
