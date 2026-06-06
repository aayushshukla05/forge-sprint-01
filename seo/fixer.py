import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:31b-cloud"
_call_count = 0

def _ask(prompt) -> str:
    global _call_count
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        _call_count += 1
        return response.json().get("response", "").strip()
    except Exception:
        return ""

def rewrite_title(url, old_title) -> str:
    prompt = (
        f"Rewrite this SEO title for the page {url}. Current title: {old_title}. "
        f"The new title must be clear, descriptive, under 60 characters, and under 561 pixels "
        f"(assume 10px per character). Return ONLY the new title text, no quotes or explanation."
    )

    result = _ask(prompt)
    if not result:
        return old_title

    if len(result) > 60:
        retry_prompt = (
            f"The previous title was too long. Please provide a shorter version under 60 "
            f"characters for {url}. Return ONLY the text."
        )
        result = _ask(retry_prompt)

    return result if (result and len(result) <= 60) else old_title

def rewrite_meta(url, old_meta) -> str:
    prompt = (
        f"Rewrite this SEO meta description for the page {url}. Current meta: {old_meta}. "
        f"The new meta description must be compelling and under 155 characters. "
        f"Return ONLY the meta description text, no quotes or explanation."
    )

    result = _ask(prompt)
    if not result:
        return old_meta

    if len(result) > 155:
        retry_prompt = (
            f"The previous meta description was too long. Please provide a shorter version "
            f"under 155 characters for {url}. Return ONLY the text."
        )
        result = _ask(retry_prompt)

    return result if (result and len(result) <= 155) else old_meta

def get_call_count() -> int:
    return _call_count
