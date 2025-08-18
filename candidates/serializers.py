from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    # Resume is automatically handled as FileField
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "resume",
            "resume_url",
            "profile_summary",
            "improvement_tips",
            "skills",
            "experience_years",
            "location_preference",
            "desired_salary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def get_resume_url(self, obj):
        request = self.context.get("request")
        if obj.resume and hasattr(obj.resume, "url"):
            return request.build_absolute_uri(obj.resume.url)
        return None
