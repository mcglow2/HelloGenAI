"""Minimal demo of talking to a llama.cpp server via its OpenAI-compatible API."""

import os
import sys

import requests
from dotenv import load_dotenv

PLACEHOLDER_KEY = "TO_BE_PROVIDED_LATER"


def load_config():
    load_dotenv()
    endpoint = os.getenv("LLAMA_ENDPOINT")
    if not endpoint:
        sys.exit("LLAMA_ENDPOINT is not set. Copy .env.example to .env and fill it in.")
    api_key = os.getenv("LLAMA_API_KEY", "")
    if api_key == PLACEHOLDER_KEY:
        api_key = ""
    return endpoint.rstrip("/"), api_key


def headers(api_key):
    h = {"Content-Type": "application/json"}
    if api_key:
        h["Authorization"] = f"Bearer {api_key}"
    return h


def check_health(endpoint, api_key):
    resp = requests.get(f"{endpoint}/health", headers=headers(api_key), timeout=10)
    print(f"Health: {resp.status_code} {resp.text.strip()}")


def list_models(endpoint, api_key):
    resp = requests.get(f"{endpoint}/v1/models", headers=headers(api_key), timeout=10)
    resp.raise_for_status()
    models = [m["id"] for m in resp.json().get("data", [])]
    print(f"Models: {', '.join(models) or '(none reported)'}")


def chat(endpoint, api_key, prompt):
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
        # Qwen3-style models "think" before answering; skip that for a quick demo.
        "chat_template_kwargs": {"enable_thinking": False},
    }
    resp = requests.post(
        f"{endpoint}/v1/chat/completions",
        headers=headers(api_key),
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    choice = resp.json()["choices"][0]
    content = choice["message"].get("content") or ""
    if not content.strip():
        reasoning = choice["message"].get("reasoning_content") or ""
        content = (
            f"(empty answer, finish_reason={choice.get('finish_reason')})"
            + (f"\nReasoning so far:\n{reasoning}" if reasoning else "")
        )
    return content


def main():
    endpoint, api_key = load_config()
    print(f"Connecting to {endpoint} (api key {'set' if api_key else 'not set'})")

    prompt = " ".join(sys.argv[1:]) or "Say hello and tell me one fun fact about llamas."
    try:
        check_health(endpoint, api_key)
        list_models(endpoint, api_key)
        print(f"\nPrompt: {prompt}\n")
        print(f"Response: {chat(endpoint, api_key, prompt)}")
    except requests.RequestException as e:
        sys.exit(f"Request failed: {e}")


if __name__ == "__main__":
    main()
