from utils.llm_utils import call_llm  # Make sure you have a utility to call Groq/OpenAI

def generate_email(topic):
    prompt = f"Write a professional email regarding: {topic}. Include a suitable subject."
    result = call_llm(prompt)
    
    lines = result.split("\n")
    subject = ""
    body = []

    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
        else:
            body.append(line)

    return {
        "subject": subject,
        "body": "\n".join(body).strip()
    }
