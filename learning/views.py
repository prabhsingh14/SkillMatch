from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from candidates.models import Candidate
from applications.models import JobApplication
from company.models import Job

from .services.build_learning_path import build_learning_path
from .serializers import LearningPathSerializer

class LearningPathView(APIView):
    def get(self, request):
        candidate_id = request.query_params.get("candidate_id")
        job_id = request.query_params.get("job_id")

        if not candidate_id or not job_id:
            return Response({
                "error": "candidate_id and job_id are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            job = Job.objects.get(id=job_id)
        except (Candidate.DoesNotExist, Job.DoesNotExist):
            return Response({
                "error": "Candidate or Job not found."
            }, status=status.HTTP_404_NOT_FOUND)

        learning_path = build_learning_path(candidate, job)
        if not learning_path:
            return Response({
                "error": "No missing skills found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = LearningPathSerializer(learning_path)
        return Response(serializer.data, status=status.HTTP_200_OK)