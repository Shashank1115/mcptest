def save_to_file(text, filename="essay.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Essay saved to {filename}")


if __name__ == "__main__":
    sample_text = "This is a sample essay text to save directly to a file."
    save_to_file(sample_text)
