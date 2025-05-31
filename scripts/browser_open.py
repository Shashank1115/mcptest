# scripts/browser_ops.py
import webbrowser

def open_browser(url="http://localhost:8000") -> str:
    webbrowser.open(url)
    return f"Browser opened at {url}"
