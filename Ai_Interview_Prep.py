# Ai_Interview_Prep.py

import streamlit as st
import tempfile
import subprocess
import os
from typing import Tuple
from PyPDF2 import PdfReader
import docx
import requests
import json

# ------------------------------------------
# CONFIG DEFAULTS
# ------------------------------------------
DEFAULT_MODEL = "llama3"
OLLAMA_METHOD = "http"      # default to HTTP
OLLAMA_HTTP_URL = "http://localhost:11434/api/generate"

# ------------------------------------------
# STREAMLIT PAGE CONFIG
# ------------------------------------------
st.set_page_config(page_title="AI Interview Curator", layout="wide")
st.title("AI Interview Question Generator — Clean Human Output")


# ------------------------------------------
# FILE TEXT EXTRACTION
# ------------------------------------------
def extract_text_from_pdf(file_obj) -> str:
    try:
        reader = PdfReader(file_obj)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"[ERROR extracting PDF text: {e}]"


def extract_text_from_docx(file_obj) -> str:
    try:
        doc = docx.Document(file_obj)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"[ERROR extracting DOCX text: {e}]"


def extract_text_from_txt(file_obj) -> str:
    try:
        return file_obj.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR extracting TXT text: {e}]"


def load_file_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    return extract_text_from_txt(uploaded_file)


# ------------------------------------------
# PROMPT (Format B)
# ------------------------------------------
def build_prompt(jd_text, resume_text, n_tech, n_behav, difficulty, include_answers):

    prompt = f"""
You are an expert technical interviewer and hiring manager.

Your job is to create a structured interview-preparation report for the candidate based on their resume and the provided job description.

======================================================
🎯 **STRICT OUTPUT FORMAT (Format B)**  
Do NOT output JSON.  
Do NOT create custom formats.  
Do NOT change section titles.  
Follow EXACTLY the structure below:

======================================================

### Candidate Fit Summary
- Strong fit: <3–5 bullet points about what makes this candidate a good match>
- Weak fit: <2–4 bullet points of gaps or risks>

---

### Technical Questions (Mandatory: Generate exactly {n_tech})
For EACH technical question, use this format:

1. <Question text tailored to the JD and resume>
- Difficulty: <easy / medium / hard — matching target: {difficulty}>
- Follow-up: <one follow-up question>
{"- Expected Answer Outline:\n  - Key point 1\n  - Key point 2\n  - Key point 3" if include_answers else ""}

(Repeat this for all {n_tech} questions.)

---

### Behavioral Questions (Mandatory: Generate exactly {n_behav})
IMPORTANT: You MUST generate behavioral questions unless {n_behav} = 0.  
If {n_behav} > 0, ALWAYS include this section and produce exactly {n_behav} questions.

For EACH behavioral question, use this format:

1. <Behavioral question tailored to the role responsibilities>
- Follow-up: <a deeper probing follow-up>

(Repeat this for all {n_behav} questions.)

======================================================

🎯 **Additional Requirements**
- Questions MUST be tailored to the candidate's resume experience.
- Questions MUST match the job description’s domain.
- Keep questions concise and practical.
- Follow the exact markdown structure above.
- Do NOT include JSON, YAML, tables, or code blocks.

======================================================

### JOB DESCRIPTION
{jd_text}

### RESUME
{resume_text}

======================================================

Now generate the final formatted interview preparation following ALL rules above.
"""
    return prompt



# ------------------------------------------
# OLLAMA CALLERS (HTTP STREAMING FIXED)
# ------------------------------------------
def call_ollama_http(model_name: str, prompt_text: str, timeout: int = 300):
    """
    Proper streaming-safe implementation for Ollama.
    """
    try:
        payload = {
            "model": model_name,
            "prompt": prompt_text,
            "stream": True
        }

        r = requests.post(
            OLLAMA_HTTP_URL,
            json=payload,
            timeout=timeout,
            stream=True
        )

        if r.status_code != 200:
            return False, f"[HTTP ERROR {r.status_code}: {r.text}]"

        full = ""

        for line in r.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    full += data["response"]
            except:
                continue

        return True, full

    except Exception as e:
        return False, f"[HTTP ERROR: {e}]"


def call_ollama_cli(model_name, prompt_text, timeout=300):
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return True, result.stdout
    except Exception as e:
        return False, f"[CLI ERROR: {e}]"


# ------------------------------------------
# UI LAYOUT
# ------------------------------------------
with st.form(key="upload_form"):

    jd_text_area = st.text_area("Paste the Job Description", height=250)
    jd_file = st.file_uploader("Or upload JD file", type=["pdf", "docx", "txt"])
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    model = st.text_input("Local model name", value=DEFAULT_MODEL)
    method = st.selectbox("Call method", ["http", "cli"])

    n_technical = st.slider("Number of technical questions", 1, 20, 10)
    n_behavioral = st.slider("Number of behavioral questions", 0, 20, 5)
    difficulty = st.selectbox("Question difficulty", ["mixed", "easy", "medium", "hard"])
    include_answers = st.checkbox("Include expected answer outlines", value=False)

    submit = st.form_submit_button("Generate Interview Questions")


# ------------------------------------------
# RUN LOGIC
# ------------------------------------------
if submit:

    jd_text = jd_text_area.strip() or load_file_text(jd_file)
    resume_text = load_file_text(resume_file)

    if not jd_text:
        st.error("Please provide a Job Description.")
        st.stop()

    if not resume_text:
        st.error("Please upload a resume.")
        st.stop()

    prompt = build_prompt(
        jd_text,
        resume_text,
        n_technical,
        n_behavioral,
        difficulty,
        include_answers
    )

    st.subheader("Prompt Preview")
    st.code(prompt[:2000] + ("\n...(truncated)" if len(prompt) > 2000 else ""))

    st.subheader("Model Response")

    if method == "cli":
        ok, out = call_ollama_cli(model, prompt)
    else:
        ok, out = call_ollama_http(model, prompt)

    if ok:
        st.markdown(out)
    else:
        st.error(out)