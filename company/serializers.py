from rest_framework import serializers
from .models import Job, Company
from core.models import Skill

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