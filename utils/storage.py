import json
import uuid
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path("sessions")
SESSIONS_DIR.mkdir(exist_ok=True)


def create_new_session(role: str):
    return {
        "session_id": str(uuid.uuid4()),
        "role": role,
        "date": datetime.now().isoformat(),
        "questions": [],
        "meta": {}
    }


def add_answer(session, question, answer_text, duration_sec, transcript_conf=1.0):
    session["questions"].append({
        "question": question,
        "answer_text": answer_text,
        "duration_sec": duration_sec,
        "transcript_confidence": transcript_conf
    })


def finalize_session(session):
    durations = [q["duration_sec"] for q in session["questions"]]

    session["meta"] = {
        "total_questions": len(durations),
        "avg_answer_duration": round(sum(durations) / len(durations), 2) if durations else 0
    }

    filename = f"session_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
    path = SESSIONS_DIR / filename

    with open(path, "w") as f:
        json.dump(session, f, indent=2)

    return path
