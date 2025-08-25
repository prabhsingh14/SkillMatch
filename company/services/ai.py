import json
from django.conf import settings
from openai import OpenAI

def _fallback_summary(job_title: str, candidates_data: list[dict]) -> str:
    lines = [f"Shortlisted summary for {job_title}"]

    #starting index from 1
    for index, candidate in enumerate(candidates_data, 1):
        skills = ", ".join(candidate.get("skills", [])[:8]) or "-"
        score = candidate.get("match_score", 0)
        score_txt = f"{score}%" if score is not None else "N/A"

        lines.append(f"{index}. {candidate.get('first_name', '')} {candidate.get('last_name', '')} | Skills: {skills} | Match Score: {score_txt}")
    
    lines.append("Overall: Compare top skills vs. JD, prioritize interviews by match score and relevant experience.")
    return "\n".join(lines)

def summarize_shortlisted_with_ai(job_title: str, candidates_data: list[dict]) -> str:
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return _fallback_summary(job_title, candidates_data)

    try:
        client = OpenAI(api_key=api_key)

        messages = [
            {"role": "system", "content": "You are an expert recruiter assistant. Be concise and structured."},
            {"role": "user", "content": (
                "Summarize shortlisted candidates for the role: '{title}'. "
                "Highlight years of experience, notable skills, and overall fit. "
                "Keep under 180 words.\n\nCandidates JSON:\n{data}"
            ).format(title=job_title, data=json.dumps(candidates_data))}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=400,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return _fallback_summary(job_title, candidates_data) + f"AI fallback due to error: {str(e)}"