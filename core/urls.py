from django.urls import path
from .views import JobFetchView

urlpatterns = [
    path('jobs/external/', JobFetchView.as_view(), name='external-job-fetch'),
]
