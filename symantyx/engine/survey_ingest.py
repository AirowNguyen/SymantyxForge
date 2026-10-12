import json
from datetime import datetime

def ingest(item):
    q = extract_question(item)
    r = extract_response(item)

    survey = {
        "id": f"survey-{datetime.utcnow().timestamp()}",
        "timestamp": datetime.utcnow().isoformat(),
        "source": item.get("source"),
        "actor": item.get("actor"),
        "question_text": q,
        "response_text": r,
        "response_type": classify_response(r),
        "survey_item": {
            "prompt": q,
            "scale": [
                "Strongly agree",
                "Agree",
                "Neutral",
                "Disagree",
                "Strongly disagree"
            ]
        },
        "cross_exam_hook": build_cross_exam_hook(q, r),
        "impeachment_value": score_impeachment(q, r)
    }

    append_to_registry(survey)
    return survey
