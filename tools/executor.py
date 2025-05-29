
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

def run_tool(tool_name, content=None):
    if tool_name == "text_generation":
        essay = generate_essay_text(content)
        context["essay"] = essay
        return essay
    elif tool_name == "notepad":
        launch_notepad()
    elif tool_name == "write_to_notepad":
        essay = context.get("essay", "No essay generated.")
        type_and_save_essay(essay)
    else:
        raise Exception(f"Unknown tool: {tool_name}")

def main():
    command = input("Enter your command: ")
    print("\n[LLM] Interpreting...")

    topic = extract_topic_from_command(command)
    print(f"\n➡️ Extracted topic: {topic}")

    run_tool("text_generation", topic)
    run_tool("notepad")
    run_tool("write_to_notepad")

if __name__ == "__main__":
    main()
