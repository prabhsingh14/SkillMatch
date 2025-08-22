import os
from PyPDF2 import PdfReader

from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Candidate
from .serializers import CandidateSerializer
from .permissions import IsCandidate
from .services.resume_parser import parse_resume_and_update

class ResumeUpload(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'candidate':
            raise PermissionDenied("Only candidates can upload resumes.")
        
        if hasattr(user, 'candidate_profile'):
            raise PermissionDenied("You already have a candidate profile.")

        serializer.save(user=user)

class ResumeAutoParseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def post(self, request):
        candidate = request.user.candidate_profile
        if not candidate.resume:
            return Response({
                "error": "No resume uploaded."
            }, status=status.HTTP_400_BAD_REQUEST)

        with candidate.resume.open('rb') as resume_file:
            result = parse_resume_and_update(candidate, resume_file)
        
        return Response(result, status=status.HTTP_200_OK)
    
class ResumeListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Candidate.objects.all()

        return Candidate.objects.filter(user=user)

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)
    
    def get_object(self):
        return get_object_or_404(self.get_queryset())