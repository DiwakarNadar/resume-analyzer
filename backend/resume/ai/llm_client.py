import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def run_llm(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("❌ OPENROUTER_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional but recommended
        "HTTP-Referer": "http://localhost",
        "X-Title": "Resume Analyzer",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ FREE
        "messages": [
            {"role": "system", "content": "You are an ATS resume evaluator."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
