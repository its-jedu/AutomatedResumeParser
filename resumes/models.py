from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

def resume_upload_path(instance, filename):
    owner = instance.owner_id or "anon"
    return f"resumes/{owner}/{filename}"

class Resume(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(["pdf","docx","txt"])]
    )
    raw_text = models.TextField(blank=True, default="")
    name = models.CharField(max_length=255, blank=True, default="")
    email = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=64, blank=True, default="")
    keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Resume({self.id})"

class MatchResult(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="matches")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="matches")
    score = models.FloatField()
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
