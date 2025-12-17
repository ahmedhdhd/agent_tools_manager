import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str, retries=3, wait_seconds=60):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()

        except ResourceExhausted as e:
            print(f"⚠️ Gemini quota exceeded. Waiting {wait_seconds}s...")
            time.sleep(wait_seconds)

    return '{"tool": null, "input": "", "done": true}'
