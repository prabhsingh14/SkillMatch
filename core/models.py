from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    candidate = models.ForeignKey('candidates.Candidate', on_delete=models.CASCADE)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate}: {self.job} ({self.status})"
    
    class Meta:
        verbose_name_plural = "Job Applications"
        ordering = ['-applied_at']
