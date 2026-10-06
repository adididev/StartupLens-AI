import os
import time
import requests


def _get_secret(key: str, default: str = "") -> str:
    """Read a secret from Streamlit Cloud (st.secrets) or fall back to env vars."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


def generate_response(query: str, context: str) -> str:
    """
    Calls the Groq chat completions API to generate a response.
    """
    api_key = _get_secret("GROQ_API_KEY")
    model = _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
    fallback_model = _get_secret("GROQ_FALLBACK_MODEL", "llama-3.1-8b-instant")
    url = "https://api.groq.com/openai/v1/chat/completions"

    if not api_key:
        return "Missing GROQ_API_KEY. Please set it in your environment before running analysis."
    
    prompt = f"""
    You are an expert startup analyst and market intelligence engine.
    Analyze the following startup idea based heavily on the provided context retrieved from the web.
    If the context isn't highly relevant to the core idea, use your base knowledge to supplement.

    Idea to analyze: {query}
    
    Context Information:
    {context}
    
    Please provide a structured market analysis with the following EXACT headers:
    
    ## 📊 Market Insights
    [Analyze the target market, size, current trends, and demand]
    
    ## ⚠️ Risks
    [List major challenges, competition, or operational risks in bullet points]
    
    ## 💡 Opportunities
    [Discuss growth potential, emerging trends, or underserved niches]
    
    ## 💰 Monetization
    [Detail possible revenue streams and pricing strategies]
    
    ## 🎯 Differentiation
    [Provide strategies on how to stand out against competitors]
    
    Do not include any other markdown headers. Keep the language professional, direct, and highly actionable.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    def _payload_for(model_name: str) -> dict:
        return {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert startup analyst and market intelligence engine."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "stream": False
        }

    max_retries = 3
    backoff_seconds = 2

    # Try preferred model first, then fallback model.
    for current_model in [model, fallback_model]:
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=_payload_for(current_model),
                    timeout=60
                )

                # Handle rate limits with retry/backoff.
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait = backoff_seconds * (2 ** attempt)
                        time.sleep(wait)
                        continue
                    break

                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except requests.exceptions.RequestException as e:
                print(f"Error calling Groq API (model={current_model}): {e}")
                if attempt < max_retries - 1:
                    wait = backoff_seconds * (2 ** attempt)
                    time.sleep(wait)
                    continue
                break

    return (
        "Groq API is currently rate-limited (HTTP 429) or unavailable. "
        "Please wait a minute and retry. You can also set a lighter model via "
        "GROQ_MODEL (for example, llama-3.1-8b-instant) to reduce rate-limit pressure."
    )
