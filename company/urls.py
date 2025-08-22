from django.urls import path
from .views import CompanyCreateView, CompanyDetailView, JobCreateView, JobListView, JobDetailView, JobAutoParseView

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/auto-parse/', JobAutoParseView.as_view(), name='job-auto-parse'),
]
