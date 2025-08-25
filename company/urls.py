from django.urls import path
from .views import (
    CompanyCreateView, CompanyDetailView, 
    JobCreateView, JobListView, JobDetailView, JobAutoParseView,
    CandidatePoolSummaryView, DashboardMetricsView, AIGeneratedSummaryView
)

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/auto-parse/', JobAutoParseView.as_view(), name='job-auto-parse'),
    path('candidates/summary/', CandidatePoolSummaryView.as_view(), name='candidate-pool-summary'),
    path('dashboard/metrics/', DashboardMetricsView.as_view(), name='dashboard-metrics'),
    path('jobs/<int:pk>/ai-summary/', AIGeneratedSummaryView.as_view(), name='ai-generated-summary'),
]
