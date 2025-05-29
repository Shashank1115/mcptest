from mcp import get_task_plan
from tools.executor import run_tool
import json
from tools.executor import extract_essay_topic
def main():
    user_input = input("Enter your command: ")
    print("\n[LLM] Interpreting...")
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