from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from candidates.models import Candidate
from company.models import Job

from .services.matching import compute_match_score

# Create your views here.
class MatchJobsToCandidateView(APIView):
    def post(self, request):
        candidate_id = request.data.get("id")
        top_n = request.data.get("limit", 5)

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

        jobs = Job.objects.filter(is_active=True)
        results = []

        for job in jobs:
            score = compute_match_score(candidate, job)
            if score > 0:
                results.append({
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company.name,
                    "match_score": score
                })
            
        results = sorted(results, key=lambda x: x['match_score'], reverse=True)[:top_n]

        return Response(results, status=status.HTTP_200_OK)

class MatchCandidatesToJobView(APIView):
    def post(self, request):
        job_id = request.data.get("id")
        top_n = request.data.get("limit", 5)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        candidates = Candidate.objects.filter(is_active=True)
        results = []

        for candidate in candidates:
            score = compute_match_score(candidate, job)
            if score > 0:
                results.append({
                    "candidate_id": candidate.id,
                    "name": str(candidate),
                    "match_score": score
                })

        results = sorted(results, key=lambda x: x['match_score'], reverse=True)[:top_n]

        return Response(results, status=status.HTTP_200_OK)