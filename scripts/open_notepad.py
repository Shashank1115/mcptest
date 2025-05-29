import subprocess

def run():
    # This command opens Notepad on Windows
    subprocess.Popen(['notepad.exe'])

if __name__ == "__main__":
    run()
