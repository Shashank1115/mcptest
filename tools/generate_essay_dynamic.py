# import openai

# openai.api_key = "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"
# openai.api_base = "https://api.groq.com/openai/v1/"


# def get_random_topic():
#     prompt = "Suggest a unique, interesting essay topic on any subject."
#     response = openai.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
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
#     model="llama3-70b-8192",  # ✅ Must be one that Groq supports
#     messages=[
#         {"role": "system", "content": "You are a helpful planner."},
#         {"role": "user", "content": "Open Notepad, write an essay, and save it."}
#     ],
#     temperature=0.5,
# )
# print(response.choices[0].message.content)


# if __name__ == "__main__":
#     print(generate_essay_text())
