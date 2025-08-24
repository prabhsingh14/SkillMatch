from django.urls import path
from .views import LearningPathView

urlpatterns = [
    path("candidates/learning-path/", LearningPathView.as_view(), name="learning-path"),
]