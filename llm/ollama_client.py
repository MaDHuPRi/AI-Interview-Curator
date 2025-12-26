import subprocess
import requests
import json
from config import OLLAMA_HTTP_URL

def call_ollama_http(model_name: str, prompt_text: str, timeout: int = 300):
    payload = {"model": model_name, "prompt": prompt_text, "stream": True}
    r = requests.post(OLLAMA_HTTP_URL, json=payload, stream=True, timeout=timeout)

    if r.status_code != 200:
        return False, r.text

    full = ""
    for line in r.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode())
            full += data.get("response", "")
        except:
            continue

    return True, full

def call_ollama_cli(model_name, prompt_text, timeout=300):
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return True, result.stdout
