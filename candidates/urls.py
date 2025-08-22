from django.urls import path
from .views import ResumeUpload, ResumeDetailView, ResumeListView, ResumeAutoParseView

urlpatterns = [
    path('resumes/upload/', ResumeUpload.as_view(), name='resume-upload'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('resumes/', ResumeListView.as_view(), name='resume-list'),
    path('resumes/parse/', ResumeAutoParseView.as_view(), name='resume-auto-parse'),
]
