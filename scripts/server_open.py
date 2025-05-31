# scripts/server_ops.py
import subprocess

def start_http_server(folder_path=".", port=8000) -> str:
    try:
        # Run server in background
        subprocess.Popen(["python", "-m", "http.server", str(port)], cwd=folder_path)
        return f"Started HTTP server at http://localhost:{port}"
    except Exception as e:
        return f"Failed to start HTTP server: {e}"
