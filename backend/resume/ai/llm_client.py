import os
import json
import requests
import re

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def parse_text_fallback(text: str) -> dict:
    """
    Parses non-JSON LLM output like:

    SUMMARY:
    - point

    STRENGTHS:
    - point
    """
    sections = {
        "summary": [],
        "strengths": [],
        "improvements": []
    }

    current = None

    for line in text.splitlines():
        line = line.strip()

        if line.upper().startswith("SUMMARY"):
            current = "summary"
            continue
        if line.upper().startswith("STRENGTHS"):
            current = "strengths"
            continue
        if line.upper().startswith("IMPROVEMENTS"):
            current = "improvements"
            continue

        if line.startswith("-") and current:
            sections[current].append(line[1:].strip())

    return sections


def clean_json(text: str) -> str:
    """
    Remove ```json fences if present
    """
    text = text.strip()
    text = re.sub(r"^```json", "", text, flags=re.I)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()


def run_llm(prompt: str) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Referer": "http://localhost:5173",
        "X-Title": "Resume Analyzer",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are an ATS resume evaluator."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    print("==== RAW LLM OUTPUT ====")
    print(content)
    print("==== END ====")

    # 1️⃣ Try JSON first
    try:
        cleaned = clean_json(content)
        parsed = json.loads(cleaned)

        return {
            "summary": parsed.get("summary", []),
            "strengths": parsed.get("strengths", []),
            "improvements": parsed.get("improvements", []),
        }

    except Exception:
        print("⚠️ JSON parse failed — falling back to text parser")

    # 2️⃣ Fallback text parser
    parsed_text = parse_text_fallback(content)

    if any(parsed_text.values()):
        return parsed_text

    # 3️⃣ Absolute fallback
    return {
        "summary": ["AI feedback unavailable"],
        "strengths": [],
        "improvements": []
    }
