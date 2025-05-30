
# import subprocess
# import pyautogui
# import time
# import requests

# API_KEY = "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"  # Replace with your actual Groq API key
# API_URL = "https://api.groq.com/openai/v1/chat/completions"

# def deepseek_query(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "llama3-70b-8192",
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 512
#     }

#     response = requests.post(API_URL, headers=headers, json=data)

#     if response.status_code != 200:
#         raise Exception(f"[Groq API Error] {response.status_code}: {response.text}")

#     return response.json()["choices"][0]["message"]["content"].strip()


# # def generate_random_topic():
# #     prompt = "Suggest a unique and interesting essay topic in one sentence."
# #     return deepseek_query(prompt)

# def generate_essay_text(topic=None):
#     if not topic:
#         topic = input("Enter your essay topic: ")
#     prompt = f"Write a detailed 300-word essay on the topic: '{topic}'"
#     essay = deepseek_query(prompt)
#     return f"Title: {topic}\n\n{essay}"

# def run_tool(tool_name, content=None):
#     if tool_name == "text_generation":
#         essay = generate_essay_text(content)
#         context["essay"] = essay
#         return essay
#     elif tool_name == "notepad":
#         launch_notepad()
#     elif tool_name == "write_to_notepad":
#         essay = context.get("essay", "No essay generated.")
#         type_and_save_essay(essay)
#     else:
#         raise Exception(f"Unknown tool: {tool_name}")

# def launch_notepad():
#     subprocess.Popen(["notepad.exe"])

# def type_and_save_essay(content):
#     time.sleep(2)  # Wait for Notepad to fully open
#     pyautogui.typewrite(content, interval=0.04)
#     time.sleep(1)
#     pyautogui.hotkey('ctrl', 's')  # Save
#     time.sleep(1)
#     pyautogui.typewrite("essay.txt")
#     pyautogui.press('enter')
#     time.sleep(1)
#     # Optionally close notepad:
#     # pyautogui.hotkey("alt", "f4")

# context = {}

# def run_tool(tool_name, content=None):
#     if tool_name == "text_generation":
#         essay = generate_essay_text()
#         context["essay"] = essay
#         return essay
#     elif tool_name == "notepad":
#         launch_notepad()
#     elif tool_name == "write_to_notepad":
#         essay = context.get("essay", "No essay generated.")
#         type_and_save_essay(essay)
#     else:
#         raise Exception(f"Unknown tool: {tool_name}")


# def main():
#     topic = input("Enter your desired essay topic: ")
#     run_tool("text_generation", topic)
#     run_tool("notepad")
#     run_tool("write_to_notepad")

# if __name__ == "__main__":
#     main()
import subprocess
import pyautogui
import time
import requests
import pyperclip
import re
from scripts.file_saver_script import save_to_file
from scripts.send_email import send_email
from scripts.generate_email import generate_email


API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def deepseek_query(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"[Groq API Error] {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()


def extract_essay_topic(command):
    # Try to find "essay on <topic>" or "write essay about <topic>" or similar phrases
    patterns = [
        r"essay on ([a-zA-Z0-9\s]+)",
        r"write essay about ([a-zA-Z0-9\s]+)",
        r"write essay on ([a-zA-Z0-9\s]+)",
        r"essay about ([a-zA-Z0-9\s]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def generate_essay_text(topic):
    prompt = f"Write a detailed 300-word essay on the topic: '{topic}'"
    essay = deepseek_query(prompt)
    return f"Title: {topic}\n\n{essay}"

def launch_notepad():
    subprocess.Popen(["notepad.exe"])

def type_and_save_essay(content):
    time.sleep(2)  # Wait for Notepad to fully open
    pyperclip.copy(content)
    pyautogui.hotkey("ctrl", "v")  # Paste instead of typing
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')  # Save
    time.sleep(1)
    pyautogui.typewrite("essay.txt")
    pyautogui.press('enter')

context = {}

# def run_tool(tool_name, content=None):
#     if tool_name == "text_generation":
#         essay = generate_essay_text(content)
#         context["essay"] = essay
#         return essay
#     elif tool_name == "notepad":
#         launch_notepad()
#     elif tool_name == "write_to_notepad":
#         essay = context.get("essay", "No essay generated.")
#         type_and_save_essay(essay)
#     else:
#         raise Exception(f"Unknown tool: {tool_name}")
def run_tool(tool_name, content=None):
    # Check if the tool_name is "text_generation"
    """
    Run a tool based on the given tool_name and content.

    Args:
        tool_name (str): The name of the tool to run.
        content (str, optional): The content to pass to the tool. Defaults to None.

    Returns:
        str: The output of the tool.

    Raises:
        Exception: If the tool_name is not recognized.
    """
    if tool_name == "text_generation":
        # Generate an essay text based on the content
        essay = generate_essay_text(content)
        # Store the essay in the context dictionary
        context["essay"] = essay
        return essay
    elif tool_name == "notepad":
        launch_notepad()
    elif tool_name == "write_to_notepad":
        essay = context.get("essay", "No essay generated.")
        type_and_save_essay(essay)
    elif tool_name == "save_file":
        save_to_file(content)
   
    elif tool_name == "generate_email":
     topic = content or "General email"
     email_data = generate_email(topic)
     context["email"] = email_data
     return email_data
    elif tool_name == "generate_email_subject":
     topic = content or "General email"
    # Use your LLM API to generate a subject based on the topic
     prompt = f"Write a suitable email subject about {topic}"
     subject = deepseek_query(prompt)
     return subject
    elif tool_name == "send_email":
        # Expecting a dict with 'to', 'subject', and 'body'
     return send_email(content["to"], content["subject"], content["body"])
    else:
        raise Exception(f"Unknown tool: {tool_name}")


def main():
    command = input("Enter your command: ")
    print("\n[LLM] Interpreting...")

    topic = extract_essay_topic(command)
    if not topic:
        print("Could not extract topic. Please try phrasing it like 'Write an essay on climate change'.")
        return

    print(f"\nExtracted topic: {topic}")

    run_tool("text_generation", topic)
    run_tool("notepad")
    run_tool("write_to_notepad")

    # Optional file saving
    run_tool("save_file", {
    "filename": "essay.txt",
    "text": context.get("essay")
})


if __name__ == "__main__":
    main()
