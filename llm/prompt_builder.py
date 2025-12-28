def build_prompt(jd_text, resume_text, n_tech, n_behav, difficulty, include_answers):
    return f"""
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