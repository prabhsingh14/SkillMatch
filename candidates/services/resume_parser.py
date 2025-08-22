import re
from PyPDF2 import PdfReader
from core.models import Skill
from core.constants import SKILL_KEYWORDS

def extract_text_from_pdf(file_obj):
    reader = PdfReader(file_obj)
    if reader.is_encrypted:
        return ""
    return "".join([page.extract_text() or "" for page in reader.pages])

def extract_skills(text: str):
    text = text.lower()
    found = []

    for canonical, keywords in SKILL_KEYWORDS.items():
        for key in keywords:
            if key.lower() in text:
                found.append(canonical)
                break
    return found

def extract_experience(text: str):
    match = re.search(r"(\d+)\+?\s*years?", text.lower())
    if match:
        return int(match.group(1))
    return 0

def parse_resume_and_update(candidate, resume_file):
    text = extract_text_from_pdf(resume_file)
    if not text.strip():
        return {"error": "Could not extract text from resume."}

    skills = extract_skills(text)
    experience = extract_experience(text)

    skills_obj = []
    for skill in skills:
        # _ here is used to ignore the second returned value (created) since we don't need it
        obj, _ = Skill.objects.get_or_create(name=skill)
        skills_obj.append(obj)
    
    candidate.skills.set(skills_obj)
    candidate.experience_years = experience
    candidate.save()

    return {
        "skills": [skill.name for skill in skills_obj],
        "experience_years": candidate.experience_years
    }
