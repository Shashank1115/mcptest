import subprocess
import pyautogui
import time
import requests
import pyperclip
import re
from scripts.file_saver_script import save_to_file
from scripts.send_email import send_email
from scripts.generate_email import generate_email
from scripts.code_generator import generate_basic_html
from scripts.project_writer import save_index_html
from scripts.vscode_open import open_vs_code
from scripts.browser_open import open_browser
from scripts.server_open import start_http_server
from scripts.text_generator import generate_text
from scripts.html_generator import generate_html
from scripts.form_builder import generate_form
from scripts.create_file import create_file
from scripts.write_to_file import write_to_file
from scripts.playwright_browser import run

import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import webbrowser
import json

API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def deepseek_query(prompt):
    # Set the headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Set the data for the API request
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    # Make the API request
    response = requests.post(API_URL, headers=headers, json=data)

    # Check if the API request was successful
    if response.status_code != 200:
        raise Exception(f"[Groq API Error] {response.status_code}: {response.text}")

    # Return the response from the API
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
def setup_hosting(content):
    # You can generate instructions or code snippets to set up hosting
    # For example, generate basic instructions to deploy on Netlify, Vercel, or GitHub Pages
    instructions = """
    To host your website:
    1. Push your code to GitHub.
    2. Use GitHub Pages or connect your repo to Netlify or Vercel.
    3. Follow their simple setup to deploy your static site.
    4. You can also use any traditional web hosting or cloud providers like AWS S3 + CloudFront.
    """
    return instructions
def generate_code(content):
    # You can implement this to generate combined HTML+CSS code or any code snippet
    # For example, just return the content or generate something based on the prompt
    return f"<!-- Generated code based on input -->\n{content}"
def run_tool(tool_name, content=None):
    if tool_name not in registry:
        raise Exception(f"Tool '{tool_name}' not found in registry.")
    
    module_path = registry[tool_name]
    module = import_module_from_path(module_path)

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
    # elif tool_name == "save_file":
    # # content must be a dict like {"text": "...", "filename": "..."}
    #  if not isinstance(content, dict):
    #     raise ValueError("Expected dict for save_to_file content")
    #  return save_to_file(content)
    # elif tool_name == "generate_essay":
    #  essay = generate_essay_text(content)
    elif tool_name == "generate_email":
     topic = content or "General email"
     email_data = generate_email(topic)
     context["email"] = email_data
     return email_data
    elif tool_name == "generate_email_subject":
     topic = content or "General email"
    # Use your LLM API to generate a subject based on the topic
     prompt = f"Write a suitable email subject about and do not write here is suitable subject directly write the subject:  {topic}"
     subject = deepseek_query(prompt)
     return subject
    elif tool_name == "send_email":
        # Expecting a dict with 'to', 'subject', and 'body'
     return send_email(content["to"], content["subject"], content["body"])
    elif tool_name == "text_generation":
        return generate_text(content)
    elif tool_name == "website_planning":
        return generate_text(content)  # Alias
    elif tool_name == "generate_html_code":
        return generate_basic_html(content)
    elif tool_name == "write_index_html":
        return save_index_html(content)
    elif tool_name == "vs_code":
        return open_vs_code(content)
    elif tool_name == "start_local_server":
        return start_http_server(content)
    elif tool_name == "open_browser":
        return open_browser(content)
    elif tool_name == "layout_design":
     return generate_text(content)
    elif tool_name == "html_generation":
     return generate_text(content)  # or a dedicated HTML generator function
    elif tool_name == "content_generation":
     return generate_text(content)
    elif tool_name == "write_to_file":
        return write_to_file(content)
    elif tool_name == "hosting_setup":
     return setup_hosting(content)
    elif tool_name == "code_generation":
        return generate_code(content) 
    elif tool_name == "create_file":
       return create_file(content)
    elif tool_name == "playwright_browser":
     return run(content)
    elif not hasattr(content, 'run'):
        raise Exception(f"Tool '{tool_name}' has no 'run' function.")

        return module.run(content)




   
    else:
        raise Exception(f"Unknown tool: {tool_name}")


def main():
    # Get user input
    command = input("Enter your command: ")
    # Print message to indicate that the command is being interpreted
    print("\n[LLM] Interpreting...")

    # Extract the topic from the user input
    topic = extract_essay_topic(command)
    # If the topic cannot be extracted, print an error message
    if not topic:
        print("Could not extract topic. Please try phrasing it like 'Write an essay on climate change'.")
        return

    # Print the extracted topic
    print(f"\nExtracted topic: {topic}")

    # Run the text generation tool with the extracted topic
    run_tool("text_generation", topic)
    # Run the notepad tool
    run_tool("notepad")
    # Run the write to notepad tool
    run_tool("write_to_notepad")

    # Optional file saving
    # Run the save file tool with the filename and text to be saved
    run_tool("save_file", {
    "filename": "essay.txt",
    "text": context.get("essay")
})


if __name__ == "__main__":
    main()
