import os
import time
import re
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "groq").lower()


def _extract_code_only(text: str) -> str:
 
    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "").strip()

    lines = text.splitlines()

    if len(lines) > 1:
        text = "\n".join(lines[1:]).strip()
    else:
        text = ""

    if not any(sym in text for sym in [";", "{", "}", "(", ")", "=", "def ", "class ", "import "]):
        raise ValueError("LLM returned non-code content")

    return text


def _ask_groq(prompt: str, retries=3):
    """
    Groq (OpenAI-compatible) – STRICT code-only output
    """
    from openai import OpenAI

    system_rule = (
        "You are a code generator.\n"
        "You MUST output ONLY valid source code.\n"
        "NO explanations.\n"
        "NO markdown.\n"
        "NO text outside code.\n"
        "If you cannot comply, output an empty string."
    )

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    for _ in range(retries):
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0,
            messages=[
                {"role": "system", "content": system_rule},
                {"role": "user", "content": prompt}
            ],
        )

        raw = response.choices[0].message.content.strip()

        try:
            return _extract_code_only(raw)
        except ValueError:
            time.sleep(1)

    raise RuntimeError("Groq failed to return valid code-only output")


def ask_llm(prompt: str) -> str:
    if LLM_MODEL == "groq":
        return _ask_groq(prompt)

    raise ValueError(f"Unsupported LLM_MODEL: {LLM_MODEL}")
