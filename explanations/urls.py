from django.urls import path
from .views import MatchExplanationView

urlpatterns = [
    path('match-explanation/', MatchExplanationView.as_view(), name='match-explanation'),
]
