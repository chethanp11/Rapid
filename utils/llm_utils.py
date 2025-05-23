# ✅ llm_utils.py — GPT Call Utility for OpenAI SDK v1.x
# ------------------------------------------------------

from openai import OpenAI
from config.pyenv import get_env

# 🔐 Load API credentials and model config from .env
api_key = get_env("OPENAI_API_KEY")
api_base = get_env("OPENAI_API_BASE", "https://api.openai.com/v1")
model = get_env("OPENAI_MODEL", "gpt-4o")
default_temp = float(get_env("OPENAI_TEMP", 0.4))
default_tokens = int(get_env("OPENAI_MAX_TOKENS", 700))

# ✅ Create OpenAI client
client = OpenAI(api_key=api_key, base_url=api_base)

def call_llm(prompt: str, temperature: float = None, max_tokens: int = None) -> str:
    """
    Calls OpenAI's chat completion endpoint using the new SDK client.
    Returns the assistant's reply or error message.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature if temperature is not None else default_temp,
            max_tokens=max_tokens if max_tokens is not None else default_tokens,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[LLM ERROR: {str(e)}]"