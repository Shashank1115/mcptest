from utils.llm_utils import call_llm

def generate_html(prompt: str) -> str:
    instruction = f"Generate clean HTML code based on the following requirement:\n\n{prompt}"
    return call_llm(instruction)
