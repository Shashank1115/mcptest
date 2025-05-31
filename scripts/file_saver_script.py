def save_to_file(text, filename="essay.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Essay saved to {filename}")


if __name__ == "__main__":
    sample_text = "This is a sample essay text to save directly to a file."
#     save_to_file(sample_text)
# def save_to_file(data, filename=None):
#     if isinstance(data, dict):
#         text = data.get("text", "")
#         filename = data.get("filename", filename or "essay.txt")
#     else:
#         text = data
#         filename = filename or "essay.txt"
    
#     if not isinstance(text, str):
#         raise TypeError("text must be a string")
    
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(text)
#     print(f"File saved to {filename}")
