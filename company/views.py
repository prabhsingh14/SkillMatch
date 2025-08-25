import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from .models import Job, Company
from applications.models import JobApplication
from candidates.models import Candidate
from .serializers import JobSerializer, CompanySerializer, JobMiniSerializer, JobApplicationMiniSerializer, CandidateMiniSerializer
from .permissions import IsEmployer
from .services.job_parser import parse_job_description_and_update
from .services.ai import summarize_shortlisted_with_ai

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from django.core.cache import cache
from django.db.models import Min

def _require_company_profile(user):
    if not hasattr(user, 'company_profile'):
        raise PermissionDenied("You must have a company profile to perform this action.")
    return user.company_profile

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

#Recruiter Intelligence Dashboard

#1. Candidate Pool Summary
class CandidatePoolSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get(self, request):
        company = _require_company_profile(request.user)

        cache_key = f"candidate_pool_summary_{company.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        
        #overall counts
        qs = JobApplication.objects.filter(job__company=company)
        total_applications = qs.count()
        total_candidates = qs.values('candidate').distinct().count()

        by_status = (
            qs.values('status').annotate(count=Count('id')).order_by()
        )
        
        status_map = {item['status']: item['count'] for item in by_status}
        shortlisted = status_map.get('shortlisted', 0)
        hired = status_map.get('hired', 0)
        rejected = status_map.get('rejected', 0)

        #per job breakdown with top 10 applications volume
        per_job = (
            qs.values('job__id', 'job__title')
                .annotate(
                    applications = Count('id'),
                    shortlisted = Count('id', filter=Q(status='shortlisted')),
                    hired = Count('id', filter=Q(status='hired')),
                    rejected = Count('id', filter=Q(status='rejected')),
                    avg_match = Avg('match_score')
                )
                .order_by('-applications')[:10]
        )

        payload = {
            "totals": {
                "total_applications": total_applications,
                "total_candidates": total_candidates,
                "shortlisted": shortlisted,
                "hired": hired,
                "rejected": rejected
            },

            "per_job": [
                {
                    "job_id": item['job__id'],
                    "job_title": item['job__title'],
                    "applications": item['applications'],
                    "shortlisted": item['shortlisted'],
                    "hired": item['hired'],
                    "rejected": item['rejected'],
                    "avg_match_score": float(item['avg_match'] or 0)
                }
                for item in per_job
            ]
        }

        #cache for 60sec
        cache.set(cache_key, payload, 60)
        return Response(payload, status=status.HTTP_200_OK)

class DashboardMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get(self, request):
        company = _require_company_profile(request.user)

        cache_key = f"dashboard_metrics_{company.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        
        apps = JobApplication.objects.filter(job__company=company)
        total_apps = apps.count()

        avg_match = apps.exclude(match_score__isnull=True).aggregate(a=Avg("match_score"))["a"] or 0
        shortlist_rate = (apps.filter(status="shortlisted").count() / total_apps * 100) if total_apps else 0
        hire_rate = (apps.filter(status="hired").count() / total_apps * 100) if total_apps else 0
        rejection_rate = (apps.filter(status="rejected").count() / total_apps * 100) if total_apps else 0

        #time-to-hire proxy (avg days b/w first app per job and first hire)
        first_app_per_job = apps.values('job').annotate(first_app=Min('applied_at'))
        hires = apps.filter(status="hired").select_related('job')

        if hires.exists() and first_app_per_job.exists():
            first_map = {item['job']: item['first_app'] for item in first_app_per_job}
            deltas = []

            for hire in hires:
                first_app = first_map.get(hire.job.id)
                if first_app:
                    delta = (hire.hired_at - first_app).days
                    deltas.append(delta)

            time_to_hire_days = round(sum(deltas) / len(deltas), 2) if deltas else None
        else:
            time_to_hire_days = None
        
        metrics = {
            "avg_match_score": round(float(avg_match), 2),
            "shortlist_rate": round(shortlist_rate, 2),
            "hire_rate": round(hire_rate, 2),
            "rejection_rate": round(rejection_rate, 2),
            "time_to_hire_days": time_to_hire_days,
        }

        cache.set(cache_key, metrics, timeout=60)
        return Response(metrics, status=status.HTTP_200_OK)

class AIGeneratedSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def post(self, request, job_id: int):
        company = _require_company_profile(request.user)
        job = get_object_or_404(Job, id=job_id, company=company)

        shortlisted = (
            JobApplication.objects.filter(job=job, status="shortlisted")
            .select_related('candidate')
            .prefetch_related('candidate__skills')
            .order_by("-match_score")
        )
        if not shortlisted.exists():
            return Response({
                "detail": "No shortlisted candidates found for this job."
            }, status=status.HTTP_404_NOT_FOUND)
        
        candidates_data = []
        for app in shortlisted[:15]:
            c = app.candidate
            candidates_data.append({
                "name": f"{c.first_name} {c.last_name}",
                "experience_years": c.experience_years,
                "skills": [s.name for s in c.skills.all()],
                "match_score": float(app.match_score) if app.match_score is not None else None,
            })

        summary = summarize_shortlisted_with_ai(job.title, candidates_data)
        
        return Response({
            "job": {"id": job.id, "title": job.title},
            "summary": summary,
            "candidates": candidates_data
        }, status=status.HTTP_200_OK)