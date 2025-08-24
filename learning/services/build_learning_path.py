from ..models import LearningResources, LearningPath, LearningStep
from candidates.models import Candidate
from company.models import Job
from .youtube import search_youtube_videos

def build_learning_path(candidate: Candidate, job: Job):
    '''
    Compare skills of candidate and those required for the job.
    Fetch YouTube resources for missing skills.
    Save them in DB if not already present.
    Build ordered learning path.
    '''

    missing_skills = job.skills.exclude(id__in=candidate.skills.all())
    if not missing_skills.exists():
        return None

    learning_path, _ = LearningPath.objects.get_or_create(candidate=candidate, job=job)
    #reset if re-building
    learning_path.resources.clear()

    order = 1
    for skill in missing_skills:
        resources = LearningResources.objects.filter(skills=skill)
        if not resources.exists():
            youtube_results = search_youtube_videos(f"{skill.name} tutorial")
            for video in youtube_results:
                resource, _ = LearningResources.objects.get_or_create(
                    title = video['title'],
                    url = video['url'],
                    difficulty = "beginner",
                )

                resource.skills.add(skill)
                resources = resources | LearningResources.objects.filter(id=resource.id)

        for resource in resources:
            LearningStep.objects.create(path=learning_path, resource=resource, order=order)
            order += 1

    return learning_path