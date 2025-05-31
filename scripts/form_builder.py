from utils.llm_utils import call_llm

def generate_form(prompt: str) -> str:
    instruction = f"Create an HTML contact form based on this description:\n\n{prompt}"
    return call_llm(instruction)
