from django.db import models
from django.conf import settings
from candidates.models import Candidate
from company.models import Job

# Create your models here.
class MatchExplanation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')
    
    def __str__(self):
        return f"MatchExplanation(candidate={self.candidate}, job={self.job})"
