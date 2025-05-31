# tools/code_generator.py

from groq import Groq  # Make sure this import matches your actual Groq SDK setup
import os

def generate_basic_html(prompt: str) -> str:
    # Securely get your API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY environment variable not set")

    # Initialize Groq client
    client = Groq(api_key=api_key)

    # Generate HTML via LLM
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": f"Generate a complete basic HTML page: {prompt}"}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
