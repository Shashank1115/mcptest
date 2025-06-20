# from mcp import get_task_plan
# from tools.executor import run_tool
# import json
# from tools.executor import extract_essay_topic
# from scripts.code_generator import generate_basic_html
# from scripts.project_writer import save_index_html
# from scripts.vscode_open import open_vs_code
# import re
# import time
# import webbrowser
# from scripts.generate_essay import generate_essay_text
# import sys
# def main():
    
#     user_input = input("Enter your command: ")
#     print("\n[LLM] Interpreting...")

#     # Website creation check
#     if re.search(r"(create|generate|build)\s+(a\s+)?(website|webpage|html\s+page)", user_input, re.I):
#         # Extract description from prompt
#         prompt_match = re.search(r"(?:for|about|on)\s+(.*)", user_input, re.I)
#         website_prompt = prompt_match.group(1).strip() if prompt_match else "simple homepage"

#         print(f"\n🛠 Generating HTML for: {website_prompt}")
#         html_code = generate_basic_html(website_prompt)

#         print("💾 Saving to index.html...")
#         project_path = save_index_html(html_code, project_name="basic_site")

#         print("🚀 Opening in VS Code...")
#         open_vs_code(project_path)

       

#         return  # Skip rest of the logic for website generation

# def main():
#     # Get user input
#     user_input = input("Enter your command: ")
#     print("\n[LLM] Interpreting...")
#     # Get task plan from user input
#     task_json = get_task_plan(user_input)

#     # Check if user input contains email keywords
#     if re.search(r"mail|email|send.*email", user_input, re.I):
#         # Extract email details: recipient, subject, body topic
#         recipient_match = re.search(r"to ([\w\.\-]+@[\w\.\-]+)", user_input, re.I)
#         recipient = recipient_match.group(1) if recipient_match else None

#         # For subject, you can use "with subject 'xxx'" or "with suitable subject"
#         subject_match = re.search(r"subject\s*['\"](.+?)['\"]", user_input, re.I)
#         subject = subject_match.group(1) if subject_match else None

#         # Extract email body topic - naive approach: after 'mail on' or 'email on'
#         topic_match = re.search(r"mail (?:on|about) ([\w\s]+)", user_input, re.I) or \
#                       re.search(r"email (?:on|about) ([\w\s]+)", user_input, re.I)
#         topic = topic_match.group(1).strip() if topic_match else "General"

#         # Generate email content
#         email_data = run_tool("generate_email", topic)

#         # If subject is missing, generate one
#         if not subject:
#             subject = run_tool("generate_email_subject", topic)

#         email_data.update({
#             "to": recipient,
#             "subject": subject
#         })

#         print(f"Generated email for recipient: {recipient}, subject: {subject}")

#         # Send the email
#         send_result = run_tool("send_email", email_data)
#         print(send_result)
#         return  # Stop further execution after email task


    

#     try:
#         # Convert task_json to a dictionary
#         task_data = json.loads(task_json)
#     except json.JSONDecodeError:
#         # Print error message if task_json is not valid JSON
#         print("[ Error] LLM did not return valid JSON:")
#         print(task_json)
#         return

#     # Check if task_data is empty or does not contain subtasks
#     if not task_data or "subtasks" not in task_data:
#         print("[ Error] Invalid task structure:")
#         print(task_data)
#         return

#     extracted_topic = extract_essay_topic(user_input)

#     print(f"\n Task: {task_data['task']}\n")

#     for subtask in task_data["subtasks"]:
#         print(f" Step {subtask['step']}: {subtask['description']}")
#         tool = subtask["tool"]
        
#         # If tool is text_generation, pass extracted topic from user command if no explicit content given
#         if tool == "text_generation":
#             content = subtask.get("content") or extracted_topic
#             if content is None:
#                 # fallback or prompt user again
#                 content = input("Enter the essay topic: ")
#             result = run_tool(tool, content)
#         else:
#             result = run_tool(tool, subtask.get("content"))

#         if result:
#             print(f" Output: {result}")

# if __name__ == "__main__":
#     main()
from mcp import get_task_plan
from tools.executor import run_tool
import json
from tools.executor import extract_essay_topic
from scripts.code_generator import generate_basic_html
from scripts.project_writer import save_index_html
from scripts.vscode_open import open_vs_code
from scripts.playwright_browser import run
import re
import time
import webbrowser
from scripts.generate_essay import generate_essay_text
import sys

def main():
    user_input = input("Enter your command: ")
    print("\n[LLM] Interpreting...")

    if "search" in user_input.lower() and "youtube" in user_input.lower():
        print("🕵️‍♂️ Running browser automation for YouTube search...")
        search_term = user_input.lower().split("search", 1)[-1].replace("on youtube", "").strip()
        result = run(search_term)
        print(f"Output: {result}")
        return


    # 1. Check if the user wants to create/generate/build a website
    if re.search(r"(create|generate|build)\s+(a\s+)?(website|webpage|html\s+page)", user_input, re.I):
        prompt_match = re.search(r"(?:for|about|on)\s+(.*)", user_input, re.I)
        website_prompt = prompt_match.group(1).strip() if prompt_match else "simple homepage"

        print(f"\n🛠 Generating HTML for: {website_prompt}")
        html_code = generate_basic_html(website_prompt)

        print("💾 Saving to index.html...")
        project_path = save_index_html(html_code, project_name="basic_site")

        print("🚀 Opening in VS Code...")
        open_vs_code(project_path)
        return

    # 2. Check if user wants to send an email
    if re.search(r"mail|email|send.*email", user_input, re.I):
        recipient_match = re.search(r"to ([\w\.\-]+@[\w\.\-]+)", user_input, re.I)
        recipient = recipient_match.group(1) if recipient_match else None

        subject_match = re.search(r"subject\s*['\"](.+?)['\"]", user_input, re.I)
        subject = subject_match.group(1) if subject_match else None

        topic_match = re.search(r"mail (?:on|about) ([\w\s]+)", user_input, re.I) or \
                      re.search(r"email (?:on|about) ([\w\s]+)", user_input, re.I)
        topic = topic_match.group(1).strip() if topic_match else "General"

        email_data = run_tool("generate_email", topic)

        if not subject:
            subject = run_tool("generate_email_subject", topic)

        email_data.update({
            "to": recipient,
            "subject": subject
        })

        print(f"Generated email for recipient: {recipient}, subject: {subject}")

        send_result = run_tool("send_email", email_data)
        print(send_result)
        return

    # 3. Otherwise, run the general task plan processing
    task_json = get_task_plan(user_input)

    try:
        task_data = json.loads(task_json)
    except json.JSONDecodeError:
        print("[ Error] LLM did not return valid JSON:")
        print(task_json)
        return

    if not task_data or "subtasks" not in task_data:
        print("[ Error] Invalid task structure:")
        print(task_data)
        return

    extracted_topic = extract_essay_topic(user_input)

    print(f"\n Task: {task_data['task']}\n")

    for subtask in task_data["subtasks"]:
        print(f" Step {subtask['step']}: {subtask['description']}")
        tool = subtask["tool"]

        if tool == "text_generation":
            content = subtask.get("content") or extracted_topic
            if content is None:
                content = input("Enter the essay topic: ")
            result = run_tool(tool, content)
        else:
            result = run_tool(tool, subtask.get("content"))

        if result:
            print(f" Output: {result}")


if __name__ == "__main__":
    main()
