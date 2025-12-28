import subprocess

def speak_text(text: str):
    try:
        subprocess.run(["say", text])
    except Exception:
        pass
