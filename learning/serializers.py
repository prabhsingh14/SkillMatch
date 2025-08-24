from rest_framework import serializers
from .models import LearningPath, LearningStep, LearningResources

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResources
        fields = ["title", "url", "platform", "difficulty", "duration_hours"]

class LearningStepSerializer(serializers.ModelSerializer):
    resource = LearningResourceSerializer()

    class Meta:
        model = LearningStep
        fields = ["order", "completed", "resource"]

class LearningPathSerializer(serializers.ModelSerializer):
    steps = LearningStepSerializer(many=True)

    class Meta:
        model = LearningPath
        fields = ["id", "candidate", "job", "steps", "created_at"]
