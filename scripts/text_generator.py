# tools/text_generator.py
from utils.llm_utils import call_llm  # Uses Groq API

def generate_text(prompt: str) -> str:
    return call_llm(prompt)
