# import time
# import pyperclip
# import pyautogui
# import subprocess
# from tools.essay_generator import generate_essay_text  # adjust if path differs

# def wait_for_notepad(window_title="Untitled - Notepad", timeout=10):
#     """Waits until Notepad window is active."""
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         windows = pyautogui.getWindowsWithTitle(window_title)
#         if windows:
#             window = windows[0]
#             if window.isActive:
#                 return True
#             else:
#                 window.activate()
#         time.sleep(0.5)
#     return False

# def write_to_notepad(text, filename="essay.txt"):
#     pyperclip.copy(text)
#     subprocess.Popen(["notepad.exe"])
#     if wait_for_notepad():
#         pyautogui.hotkey("ctrl", "v")
#         time.sleep(1)
#         pyautogui.hotkey("ctrl", "s")
#         time.sleep(1)
#         pyautogui.write(filename)
#         pyautogui.press("enter")
#         time.sleep(1)
#         pyautogui.hotkey("alt", "f4")
#     else:
#         print("Notepad did not open in time.")

# if __name__ == "__main__":
#     topic = input("Enter the essay topic: ")
#     essay = generate_essay_text(topic)
#     write_to_notepad(essay)
import time
import pyperclip
import pyautogui
import subprocess
from generate_essay import generate_essay_text   # adjust path if needed

def wait_for_notepad(window_title="Untitled - Notepad", timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        windows = pyautogui.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]
            if window.isActive:
                return True
            else:
                window.activate()
        time.sleep(0.5)
    return False

def write_to_notepad(text, filename="essay.txt"):
    try:
        pyperclip.copy(text)
        subprocess.Popen(["notepad.exe"])
        if wait_for_notepad():
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1)
            pyautogui.write(filename)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.hotkey("alt", "f4")
        else:
            print("Notepad did not open in time.")
    except Exception as e:
        print(f"Error during Notepad operation: {e}")

if __name__ == "__main__":
    topic = input("Enter the essay topic: ").strip()
    if not topic:
        print(" No topic provided. Please enter a valid topic.")
    else:
        essay = generate_essay_text(topic)
        filename = input("Enter filename (default: essay.txt): ").strip() or "essay.txt"
        write_to_notepad(essay, filename)
