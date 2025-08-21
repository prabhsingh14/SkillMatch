from candidates.models import Candidate
from company.models import Job
from applications.models import JobApplication

def compute_match_score(candidate: Candidate, job: Job) -> float:
    score = 0.0
    weight_skills, weight_exp, weight_loc, weight_salary = 0.5, 0.25, 0.15, 0.10

    #skills
    candidate_skills = set(candidate.skills.values_list('id', flat=True))
    job_skills = set(job.skills.values_list('id', flat=True))
    if job_skills:
        overlap = candidate_skills.intersection(job_skills)
        skill_score = len(overlap) / len(job_skills)
        score += skill_score * weight_skills
    
    #experience
    job_exp_req = job.match_criteria.get('experience_years') if job.match_criteria else 0
    if job_exp_req > 0:
        diff = abs(candidate.experience_years - job_exp_req)
        exp_score = max(0, 1 - (diff / max(1, job_exp_req)))
        score += exp_score * weight_exp
    
    #location
    if candidate.location_preference and candidate.location_preference.lower() == job.location.lower():
        score += 1.0 * weight_loc #full score if location matches

    #salary
    if candidate.desired_salary and job.salary:
        if candidate.desired_salary <= job.salary:
            score += 1.0 * weight_salary
    
    return round(score * 100, 2) #scale 0-100