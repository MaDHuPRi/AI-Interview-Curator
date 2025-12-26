# app.py

import streamlit as st
import re

from config import DEFAULT_MODEL
from loaders.file_loader import load_file_text
from llm.prompt_builder import build_prompt
from llm.ollama_client import call_ollama_http, call_ollama_cli
from tts.speaker import speak_text
from stt.whisper_stt import record_audio, transcribe

# ------------------------------------------
# STREAMLIT CONFIG
# ------------------------------------------
st.set_page_config(page_title="AI Interview Prep", layout="wide")
st.title("🎤 AI Interview Prep — Mock Interviewer")

# ------------------------------------------
# SESSION STATE
# ------------------------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "review"   # review | interview

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0

if "spoken" not in st.session_state:
    st.session_state.spoken = False

if "instructions_spoken" not in st.session_state:
    st.session_state.instructions_spoken = False


# ------------------------------------------
# HELPERS
# ------------------------------------------
def extract_all_questions(model_output: str):
    """
    Extracts all numbered questions from the LLM output.
    """
    return re.findall(r"\n\d+\.\s+(.*)", model_output)

INSTRUCTION_TEXT = (
    "Before we begin, here is how the mock interview will work. "
    "I will ask you one question at a time. "
    "After each question, click the start recording button and you will have up to one minute to answer. "
    "Once you finish answering, press the continue button to move to the next question. "
    "When you are ready, we will begin with the first question."
)



# ------------------------------------------
# INPUT FORM (GENERATION)
# ------------------------------------------
with st.form("generation_form"):
    jd_text_area = st.text_area("Paste Job Description", height=200)
    jd_file = st.file_uploader("Or upload JD", type=["pdf", "docx", "txt"])
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    model = st.text_input("Local model name", value=DEFAULT_MODEL)
    method = st.selectbox("Ollama call method", ["http", "cli"])

    n_technical = st.slider("Technical questions", 1, 10, 5)
    n_behavioral = st.slider("Behavioral questions", 0, 5, 2)
    difficulty = st.selectbox("Difficulty", ["mixed", "easy", "medium", "hard"])
    include_answers = st.checkbox("Include answer outlines", value=False)

    submitted = st.form_submit_button("Generate Interview")

# ------------------------------------------
# GENERATE + DISPLAY (REVIEW PHASE)
# ------------------------------------------
if submitted:
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

    st.subheader("🧠 LLM Prompt (Preview)")
    st.code(prompt[:1500] + ("..." if len(prompt) > 1500 else ""))

    if method == "cli":
        ok, output = call_ollama_cli(model, prompt)
    else:
        ok, output = call_ollama_http(model, prompt)

    if not ok:
        st.error(output)
        st.stop()

    # Display everything (silent)
    st.subheader("📋 Interview Preparation")
    st.markdown(output)

    # Parse and store questions
    st.session_state.questions = extract_all_questions(output)
    st.session_state.phase = "review"
    st.session_state.current_q_index = 0
    st.session_state.spoken = False

# ------------------------------------------
# START MOCK INTERVIEW BUTTON (AFTER REVIEW)
# ------------------------------------------
if st.session_state.questions and st.session_state.phase == "review":
    st.divider()
    if st.button("🎙 Start Mock Interview"):
        st.session_state.phase = "instructions"
        st.rerun()

# ------------------------------------------
# INSTRUCTION PHASE (VOICE STARTS HERE)
# ------------------------------------------
if st.session_state.phase == "instructions":

    st.subheader("📢 Interview Instructions")
    st.write(INSTRUCTION_TEXT)

    # Speak instructions only once
    if not st.session_state.instructions_spoken:
        speak_text(INSTRUCTION_TEXT)
        st.session_state.instructions_spoken = True

    if st.button("Continue to Interview"):
        st.session_state.phase = "interview"
        st.session_state.spoken = False
        st.rerun()

# ------------------------------------------
# MOCK INTERVIEW PHASE (VOICE STARTS HERE)
# ------------------------------------------
if st.session_state.phase == "interview":
    questions = st.session_state.questions
    q_idx = st.session_state.current_q_index

    if q_idx < len(questions):
        question = questions[q_idx]

        st.subheader(f"🎙 Interviewer — Question {q_idx + 1}")
        st.write(question)

        # Speak only once per question
        if not st.session_state.spoken:
            speak_text(question)
            st.session_state.spoken = True

        st.subheader("🧑 Your Answer")
        if "last_answer" not in st.session_state and st.button("Start Recording"):
            st.info("Recording... Speak now.")
            audio_path = record_audio(duration=60)
            transcript = transcribe(audio_path)

            st.session_state.last_answer = transcript
            st.success("Recording complete")

        if "last_answer" in st.session_state:
            st.text_area(
                "Transcribed Answer",
                value=st.session_state.last_answer,
                height=150,
                key=f"transcript_{q_idx}"
            )

        if st.button("Next Question"):
            st.session_state.current_q_index += 1
            st.session_state.spoken = False
            st.session_state.pop("last_answer", None)  # 👈 ADD THIS
            st.rerun()


    else:
        st.success("🎉 Mock Interview Complete")
        st.write("Great job completing the interview!")
