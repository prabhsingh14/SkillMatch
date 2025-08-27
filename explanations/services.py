import os
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_match_explanation(candidate_skills, job_requirements):
    prompt = f"""
    Explain in simple, clear language why a candidate with skills {candidate_skills}
    is a good match (or not) for a job with requirements {job_requirements}.
    Highlight overlaps and gaps in 4-5 sentences.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast + cheap
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
