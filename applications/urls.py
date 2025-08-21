from django.urls import path
from applications.views import MatchJobsToCandidateView, MatchCandidatesToJobView

urlpatterns = [
    path("match/jobs/", MatchJobsToCandidateView.as_view(), name="match-jobs-to-candidate"),
    path("match/candidates/", MatchCandidatesToJobView.as_view(), name="match-candidates-to-job"),
]
