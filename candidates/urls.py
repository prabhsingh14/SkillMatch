from django.urls import path
from .views import ResumeUpload, ResumeParser, ResumeDetailView, ResumeListView

urlpatterns = [
    path('resumes/upload/', ResumeUpload.as_view(), name='resume-upload'),
    path('resumes/parse/', ResumeParser.as_view(), name='resume-parse'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('resumes/', ResumeListView.as_view(), name='resume-list'),
]
