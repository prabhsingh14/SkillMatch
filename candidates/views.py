import os
from PyPDF2 import PdfReader

from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

from .models import Candidate
from .serializers import CandidateSerializer
from .permissions import IsCandidate

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

class ResumeParser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({
                "error": "No resume file provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        file_ext = os.path.splitext(resume_file.name)[1].lower()
        if file_ext != ".pdf":
            return Response({
                "error": "Only PDF files are allowed."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        extracted_text = ""
        
        try:
            pdf_reader = PdfReader(resume_file)
            if pdf_reader.is_encrypted:
                return Response({
                    "error": "The PDF file is encrypted and cannot be processed."
                }, status=status.HTTP_400_BAD_REQUEST)

            extracted_text =  " ".join([page.extract_text() or "" for page in pdf_reader.pages])

        except Exception as e:
            return Response({
                "error": "Failed to extract text from PDF."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "extracted_text": extracted_text
        }, status=status.HTTP_200_OK)

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