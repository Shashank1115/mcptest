# import openai

# openai.api_key = "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"
# openai.api_base = "https://api.groq.com/openai/v1/"


# def get_random_topic():
#     prompt = "Suggest a unique, interesting essay topic on any subject."
#     response = openai.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=20,
#         temperature=0.9,
#         n=1,
#     )
#     topic = response.choices[0].message.content.strip().strip('"').strip("'")
#     return topic


# def generate_essay_text():
#     topic = get_random_topic()
#     prompt = f"Write a detailed 300-word essay on the topic: '{topic}'. Make it informative and well-structured."
#     response = openai.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.5,
#         max_tokens=200,
#     )
#     return f"Title: {topic}\n\n{response.choices[0].message.content.strip()}"


# if __name__ == "__main__":
#     print(generate_essay_text())
# tools/essay_generator.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads API key from .env
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1/"

def generate_essay_text(user_prompt: str) -> str:
    """Generate a detailed 200-word essay based on user prompt."""
    system_message = "You are a helpful assistant who writes well-structured, informative essays."
    prompt = f"Write a detailed 300-word essay on the topic: '{user_prompt}'."

    response = openai.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=600,  # Increased to allow enough space for a ~300-word essay
    )

    return f"Title: {user_prompt}\n\n{response.choices[0].message.content.strip()}"

if __name__ == "__main__":
    # Take user input from command line
    user_input = input("Enter an essay topic: ")
    essay = generate_essay_text(user_input)
    print(essay)
