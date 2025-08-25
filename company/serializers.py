from rest_framework import serializers
from .models import Job, Company
from core.models import Skill
from candidates.models import Candidate
from applications.models import JobApplication

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ["user", "created_at", "updated_at"]

class JobSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = [
            "company",
            "created_at",
            "updated_at",
            "source",
            "source_url",
            "posted_at"
        ]

class CandidateMiniSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'experience_years', 'skills']

class JobMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'employment_type', 'is_active']

class JobApplicationMiniSerializer(serializers.ModelSerializer):
    candidate = CandidateMiniSerializer(read_only=True)
    job = JobMiniSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'candidate', 'job', 'status', 'match_score', 'applied_at']