from django.db import models
from django.conf import settings

from candidates.models import Candidate
from company.models import Job
from core.models import Skill

# Create your models here.
class LearningResources(models.Model):
    PLATFORM_CHOICES = [
        ("udemy", "Udemy"),
        ("youtube", "YouTube"),
        ("coursera", "Coursera"),
        ("github", "GitHub"),
        ("doc", "Official Docs"),
        ("whitepaper", "Whitepaper")
    ]

    title = models.CharField(max_length=255)
    url = models.URLField()
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default="youtube")
    skills = models.ManyToManyField(Skill, related_name='learning_resources')
    difficulty = models.CharField(max_length=50, choices=[
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced")
    ])
    duration_hours = models.PositiveIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"

class LearningPath(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resources = models.ManyToManyField(LearningResources, related_name='learning_paths')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Learning Path for {self.candidate} - {self.job}"

class LearningStep(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    resource = models.ForeignKey(LearningResources, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.order} for {self.path}"