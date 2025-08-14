from django.contrib import admin
from .models import User, CandidateProfile, CompanyProfile

# Register your models here.
admin.site.register(User)
admin.site.register(CandidateProfile)
admin.site.register(CompanyProfile)
