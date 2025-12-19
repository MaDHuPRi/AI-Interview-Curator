
# AI Interview Curator

A **Streamlit-based AI interview preparation tool** that analyzes a **Job Description** and a **resume** to generate:

- ✔️ Candidate fit summary  
- ✔️ Good-fit & weak-fit breakdown  
- ✔️ Tailored **technical questions** (with difficulty + follow-ups)  
- ✔️ Tailled **behavioral questions** (with follow-ups)  
- ✔️ Optional **expected answer outlines**  
- ✔️ Clean Format-B structured output  
- ✔️ Runs locally using **Ollama** (no cloud, fully private)

Built for students, job-seekers, and engineers who want **realistic, role-specific interview prep** generated entirely on their machine.

---

## How It Works

1. Upload or paste:
   - A **Job Description**
   - Your **resume** (PDF, DOCX, or TXT)

2. Select:
   - Number of technical questions  
   - Number of behavioral questions  
   - Difficulty level  
   - Whether to include expected answers  

3. Click **Generate**  
   The app uses Ollama (local LLMs) to produce a crisply formatted interview-prep document.

---

## 🛠️ Tech Stack

- **Python**  
- **Streamlit** (UI)  
- **Ollama** (local model inference)  
- **LLMs** (e.g., Llama 3, Qwen, Mistral, etc.)  
- **PyPDF2 / python-docx** for file parsing  

---

## 📁 Project Structure

```
ai_interview/
│
├── app.py                    # Main Streamlit app (thin UI layer)
│
├── config.py                 # Constants & defaults
│
├── loaders/
│   ├── __init__.py
│   └── file_loader.py        # PDF / DOCX / TXT extraction
│
├── llm/
│   ├── __init__.py
│   ├── prompt_builder.py     # Prompt construction
│   └── ollama_client.py      # Ollama HTTP / CLI calls
│
├── tts/
│   ├── __init__.py
│   └── speaker.py            # TTS logic
│
├── interview/
│   ├── __init__.py
│   └── question_parser.py    # Extract first question
│
└── requirements.txt

```

---

## ⚙️ Installation

### 1. Install Python packages  
```
pip install streamlit PyPDF2 python-docx requests
```

### 2. Install Ollama  
Download from:  
https://ollama.com/download

### 3. Pull a model (example)  
```
ollama pull llama3
```

### 4. Run the app  
```
streamlit run Ai_Interview_Prep.py
```

---

## Features

### Candidate Fit Summary
- Highlights strengths across skills, tools, and experience  
- Identifies gaps or mismatches  

### Technical Questions
Each question includes:
- Difficulty  
- Follow-up question  
- (Optional) expected answer outline  

Questions are fully **tailored to the JD & resume**.

### Behavioral Questions
- STAR-style follow-ups  
- Role-specific behavioral prompts  

### 100% Local
Your resume and JD **never leave your machine**.  
Ollama handles everything locally.

---

## Example Use Cases

- Preparing for software engineering, data, ML, DevOps, or PM interviews  
- Getting a fast “mock interview prep sheet” from any job posting  
- Practicing with role-specific, realistic questions  
- Reviewing job fit and skill gaps  

---

## Customize It

Want to add:
- PDF export  
- Difficulty color badges  
- Custom question categories  
- Multiple model support  
- STAR-format answer breakdowns  

Just ask! The project is easy to extend.

---

## Contributing

PRs welcome!  
You can contribute by:
- Adding new question styles  
- Improving prompts  
- Supporting additional file types  
- Enhancing UI/UX  

---

x
