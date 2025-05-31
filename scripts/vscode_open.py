import subprocess

def open_vs_code(path="..") -> str:
    try:
        subprocess.Popen(f"code {path}", shell=True)
        return "VS Code opened."
    except Exception as e:
        return f"Failed to open VS Code: {e}"
