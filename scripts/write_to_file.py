def write_to_file(params: dict) -> str:
    if not isinstance(params, dict):
        return "Invalid input: expected a dictionary with filename and content."

    filename = params.get("filename")
    content = params.get("content")

    if not filename or not content:
        return "Missing filename or content."

    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing to file: {e}"
