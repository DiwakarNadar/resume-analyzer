from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


def default_expiry():
    return timezone.now() + timedelta(days=7)


class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session_id = models.UUIDField(default=uuid.uuid4, editable=False)

    original_file_name = models.CharField(max_length=255, blank=True)

    file = models.CharField(max_length=500)  # ⬅ Supabase file path / URL

    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True)

    skills = models.JSONField(default=list)
    ats_score = models.IntegerField(null=True, blank=True)
    analysis_result = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return f"Resume {self.id}"

class JDComparison(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session_id = models.UUIDField(db_index=True)
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="comparisons"
    )

    job_description = models.TextField()

    match_percentage = models.FloatField()
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JD Comparison {self.id}"
