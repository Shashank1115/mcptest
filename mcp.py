import requests
import json

api_key = "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"
base_url = "https://api.groq.com/openai/v1/chat/completions"

def get_task_plan(user_input):
    prompt = f"""
You are an intelligent task planner that breaks down high-level commands into actionable tool-based subtasks for agents. 
Given a user input, return a JSON with:

- task: a one-line summary
- subtasks: a list of steps with:
    - step (number),
    - description,
    - agent (LLM or SystemAgent),
    - tool (script/tool to run)

ONLY respond in **valid JSON** format. Do **not** add any explanation, markdown, or formatting and every one must have key value pair and only and do not change tool name every time make it same .
Input: "{user_input}"

Respond ONLY in this JSON format:
{{
  "task": "Write an essay in Notepad",
  "subtasks": [
    {{
      "step": 1,
      "description": "Open Notepad",
      "agent": "SystemAgent",
      "tool": "notepad"
    }},
    {{
      "step": 2,
      "description": "Generate an essay",
      "agent": "LLM",
      "tool": "text_generation"
    }},
    {{
      "step": 3,
      "description": "Write the essay into Notepad",
      "agent": "SystemAgent",
      "tool": "write_to_notepad"
    }},
    {{
      "step": 4,
      "description": "Save the file",
      "agent": "SystemAgent",
      "tool": "save_file"
    }}
  ]
}}
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful planning assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 600,
    }

    response = requests.post(base_url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    user_input = input("Enter your task: ")
    task_plan = get_task_plan(user_input)
    print(task_plan)

