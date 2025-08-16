from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Only PDF files are allowed.")

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/', validators=[validate_pdf])
    profile_summary = models.TextField(blank=True, null=True)  # AI-generated or self-written
    improvement_tips = models.JSONField(default=list, blank=True)  # AI suggestions
    skills = models.ManyToManyField('core.Skill', related_name='candidates')
    experience_years = models.PositiveIntegerField(default=0)
    location_preference = models.CharField(max_length=100, blank=True, null=True)
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']
