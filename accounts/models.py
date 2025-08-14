from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CANDIDATE = "candidate", "Candidate"
        COMPANY = "company", "Company"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE
    )

    def is_candidate(self):
        return self.role == self.Role.CANDIDATE

    def is_company(self):
        return self.role == self.Role.COMPANY

    def is_admin(self):
        return self.role == self.Role.ADMIN

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    resume = models.FileField(upload_to="resumes/")
    bio = models.TextField(blank=True)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True)