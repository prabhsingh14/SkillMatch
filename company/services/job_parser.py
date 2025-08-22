from core.models import Skill
from core.constants import SKILL_KEYWORDS
import re

def extract_job_skills(text):
    text = text.lower()
    found = []

    for canonical, keywords in SKILL_KEYWORDS.items():
        for key in keywords:
            if key.lower() in text:
                found.append(canonical)
                break
    return found

def extract_job_experience(text):
    match = re.search(r"(\d+)\+?\s*years?", text.lower())
    return int(match.group(1)) if match else 0

def parse_job_description_and_update(job):
    job = job.description or ""
    skills = extract_job_skills(job)
    experience = extract_job_experience(job)

    skills_obj = []
    for skill in skills:
        obj, _ = Skill.objects.get_or_create(name=skill)
        skills_obj.append(obj)

    job.skills.set(skills_obj)
    job.match_criteria = {"experience_years": experience} if experience > 0 else {}
    job.save()

    return {
        "skills": [skill.name for skill in skills_obj],
        "match_criteria": job.match_criteria
    }
