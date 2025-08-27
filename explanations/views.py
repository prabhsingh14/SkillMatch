from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from candidates.models import Candidate
from company.models import Job
from .models import MatchExplanation
from .services import generate_match_explanation

# Create your views here.

class MatchExplanationView(APIView):
    def post(self, request):
        candidate_id = request.data.get('candidate_id')
        job_id = request.data.get('job_id')

        candidate = Candidate.objects.filter(id=candidate_id).first()
        job = Job.objects.filter(id=job_id).first()

        if not candidate or not job:
            return Response({"error": "Invalid candidate or job ID"}, status=status.HTTP_400_BAD_REQUEST)

        candidate_skills = [skill.name for skill in candidate.skills.all()]
        job_requirements = [skill.name for skill in job.skills.all()]

        #check if explanation already exists
        explanation_obj, created = MatchExplanation.objects.get_or_create(
            candidate=candidate,
            job=job,
            defaults={'explanation': generate_match_explanation(candidate_skills, job_requirements)}
        )

        if created or not explanation_obj.explanation:
            explanation_text = generate_match_explanation(candidate_skills, job_requirements)
            explanation_obj.explanation = explanation_text
            explanation_obj.save()

        return Response({
            "candidate": candidate.name,
            "job": job.title,
            "explanation": explanation_obj.explanation
        }, status=status.HTTP_200_OK)