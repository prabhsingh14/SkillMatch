from django.db import models
from django.conf import settings

class JobApplication(models.Model):
    candidate = models.ForeignKey('candidates.Candidate', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey('company.Job', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ], default='applied', db_index=True)
    match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)  # Recruiter feedback
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate} → {self.job} ({self.status})"

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-applied_at']
