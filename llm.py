import os
import time
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "gemini").lower()

 
def _ask_gemini(prompt: str, retries=3, wait_seconds=60):
    import google.generativeai as genai
    from google.api_core.exceptions import ResourceExhausted

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    system_rule = (
        "You are a code generator.\n"
        "You MUST output ONLY valid source code.\n"
        "NO explanations.\n"
        "NO markdown.\n"
        "NO comments unless they are code comments.\n"
        "If you cannot comply, output an empty string."
    )

    for _ in range(retries):
        try:
            response = model.generate_content(system_rule + "\n\n" + prompt)
            return _extract_code_only(response.text)
        except ResourceExhausted:
            print(f"⚠️ Gemini quota exceeded. Waiting {wait_seconds}s...")
            time.sleep(wait_seconds)
        except ValueError:
            print("⚠️ Non-code output detected. Retrying...")
            time.sleep(1)

    raise RuntimeError("Gemini failed to return valid code")

 


def _ask_groq(prompt: str, retries=3):
    """
    Groq (OpenAI-compatible) – STRICT code-only output
    """
    import os
    import time
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
            model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
            temperature=0,
            messages=[
                {"role": "system", "content": system_rule},
                {"role": "user", "content": prompt}
            ],
        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```", "").strip()

        if any(sym in content for sym in [";", "{", "}", "(", ")", "=", "def ", "class ", "import "]):
            return content

        time.sleep(1)

    raise RuntimeError("Groq failed to return valid code-only output")

import re

def _extract_code_only(text: str) -> str:
    """
    Enforces code-only output.
    Removes markdown, explanations, and rejects non-code responses.
    """
    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "").strip()

    if not any(sym in text for sym in [";", "{", "}", "(", ")", "=", "def ", "class ", "import "]):
        raise ValueError("LLM returned non-code content")

    return text

 
def ask_llm(prompt: str) -> str:
    if LLM_MODEL == "gemini":
        return _ask_gemini(prompt)

    if LLM_MODEL == "grok":
        return _ask_grok(prompt)
        
    if LLM_MODEL == "groq":
        return _ask_groq(prompt)

    raise ValueError(f"Unsupported LLM_MODEL: {LLM_MODEL}")
