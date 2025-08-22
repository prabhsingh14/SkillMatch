import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from .models import Job, Company
from .serializers import JobSerializer, CompanySerializer
from .permissions import IsEmployer
from .services.job_parser import parse_job_description_and_update

from django.conf import settings
from django.shortcuts import get_object_or_404

class IsAdminUser(permissions.BasePermission):
    """
    Allow only admin/superuser to perform this action
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

#company profile management
class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'company_profile'):
            raise PermissionDenied("You already have a company profile.")
        
        serializer.save(user=user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)

'''PARSE'''

class JobAutoParseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
        result = parse_job_description_and_update(job, request.data)
        return Response(result, status=status.HTTP_200_OK)

#job management
class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "employer":
            raise PermissionDenied("You do not have permission to create a job.")

        if not hasattr(user, 'company_profile'):
            raise PermissionDenied("You must have a company profile to create a job.")
        
        serializer.save(company=user.company_profile, source="internal")

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company_profile'):
            return Job.objects.filter(company=user.company_profile)
        return Job.objects.none()

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company_profile'):
            return Job.objects.filter(company=user.company_profile)
        return Job.objects.none()