from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']

    if not ext.lower() in valid_extensions:
        raise ValidationError("Only PDF files are allowed.")

# Create your models here.
class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    skills = models.ManyToManyField('core.Skill', related_name='candidates')
    experience_years = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']
