import re

def extract_first_question(model_output: str) -> str | None:
    match = re.search(r"\n1\.\s+(.*)", model_output)
    if match:
        return match.group(1).strip()
    return None
