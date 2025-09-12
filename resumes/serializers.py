from rest_framework import serializers
from .models import Resume, Job, MatchResult

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id","title","description","keywords","created_at"]

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id","file","name","email","phone","skills","raw_text","created_at"]
        read_only_fields = ["raw_text","email","phone","skills"]

class ResumeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id","name","email","phone","skills","raw_text","created_at","file"]

class MatchResultSerializer(serializers.ModelSerializer):
    resume = ResumeDetailSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = MatchResult
        fields = ["id","resume","job","score","details","created_at"]
