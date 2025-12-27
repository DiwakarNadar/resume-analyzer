from rest_framework import serializers
from .models import Resume


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "session_id", "file", "uploaded_at"]
        read_only_fields = ["id", "session_id", "uploaded_at"]
