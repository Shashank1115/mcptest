from mcp import get_task_plan
from tools.executor import run_tool
import json
from tools.executor import extract_essay_topic
import re
def main():
    user_input = input("Enter your command: ")
    print("\n[LLM] Interpreting...")
    task_json = get_task_plan(user_input)

    if re.search(r"mail|email|send.*email", user_input, re.I):
        # Extract email details: recipient, subject, body topic
        recipient_match = re.search(r"to ([\w\.\-]+@[\w\.\-]+)", user_input, re.I)
        recipient = recipient_match.group(1) if recipient_match else None

        # For subject, you can use "with subject 'xxx'" or "with suitable subject"
        subject_match = re.search(r"subject\s*['\"](.+?)['\"]", user_input, re.I)
        subject = subject_match.group(1) if subject_match else None

        # Extract email body topic - naive approach: after 'mail on' or 'email on'
        topic_match = re.search(r"mail (?:on|about) ([\w\s]+)", user_input, re.I) or \
                      re.search(r"email (?:on|about) ([\w\s]+)", user_input, re.I)
        topic = topic_match.group(1).strip() if topic_match else "General"

        # Generate email content
        email_data = run_tool("generate_email", topic)

        # If subject is missing, generate one
        if not subject:
            subject = run_tool("generate_email_subject", topic)

        email_data.update({
            "to": recipient,
            "subject": subject
        })

        print(f"Generated email for recipient: {recipient}, subject: {subject}")

        # Send the email
        send_result = run_tool("send_email", email_data)
        print(send_result)
        return  # Stop further execution after email task


    

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
        
        # If tool is text_generation, pass extracted topic from user command if no explicit content given
        if tool == "text_generation":
            content = subtask.get("content") or extracted_topic
            if content is None:
                # fallback or prompt user again
                content = input("Enter the essay topic: ")
            result = run_tool(tool, content)
        else:
            result = run_tool(tool, subtask.get("content"))

        if result:
            print(f" Output: {result}")

if __name__ == "__main__":
    main()