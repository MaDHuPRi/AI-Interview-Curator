import json
import re
from llm.ollama_client import call_ollama_http

def evaluate_answer(question: str, answer: str, model: str):
    prompt = f"""
You are an interview evaluator.

Evaluate the following answer on a scale of 0 to 10(integers only) for:
1. Clarity
2. Confidence
3. Technical Depth

Then provide:
- One short strength
- One specific improvement suggestion

Return ONLY valid JSON in this exact format:

{{
  "clarity": 0,
  "confidence": 0,
  "technical_depth": 0,
  "strength": "",
  "improvement": ""
}}

Question:
{question}

Answer:
{answer}
"""

    ok, response = call_ollama_http(model, prompt)

    if not ok:
        raise RuntimeError(response)

    # ✅ Extract JSON safely
    match = re.search(r"\{[\s\S]*\}", response)

    if not match:
        raise ValueError(f"No JSON found in LLM output:\n{response}")

    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by LLM:\n{match.group()}") from e
