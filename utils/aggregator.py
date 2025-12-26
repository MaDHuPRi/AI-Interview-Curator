def aggregate_feedback(questions):
    if not questions:
        return {}

    clarity_scores = []
    confidence_scores = []
    technical_scores = []
    strengths = []
    improvements = []

    for q in questions:
        eval_data = q.get("evaluation", {})
        if not eval_data:
            continue

        clarity_scores.append(eval_data.get("clarity", 0))
        confidence_scores.append(eval_data.get("confidence", 0))
        technical_scores.append(eval_data.get("technical_depth", 0))

        strengths.append(eval_data.get("strength", ""))
        improvements.append(eval_data.get("improvement", ""))

    def avg(arr):
        return round(sum(arr) / len(arr), 1) if arr else 0.0

    avg_clarity = avg(clarity_scores)
    avg_confidence = avg(confidence_scores)
    avg_technical = avg(technical_scores)

    overall_score = round(
        (avg_clarity + avg_confidence + avg_technical) / 3, 2
    )

    summary = generate_summary(
        avg_clarity, avg_confidence, avg_technical
    )

    return {
        "avg_clarity": avg_clarity,
        "avg_confidence": avg_confidence,
        "avg_technical_depth": avg_technical,
        "overall_score": overall_score,
        "summary": summary,
        "strengths": list(set(filter(None, strengths))),
        "improvements": list(set(filter(None, improvements)))
    }


def generate_summary(clarity, confidence, technical):
    if clarity > 0.8 and technical > 0.8:
        return "Excellent clarity and strong technical depth. Answers are well-structured and confident."
    if clarity > 0.8:
        return "Strong communication skills with clear explanations, but technical depth can be improved."
    if technical > 0.8:
        return "Good technical understanding, but explanations could be clearer and more structured."
    if confidence < 0.6:
        return "Answers show hesitation. Improving confidence and delivery will help significantly."
    return "Overall performance is solid, with room for improvement in clarity and technical depth."
