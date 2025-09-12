from django.contrib import admin
from .models import Job, Resume, MatchResult

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id","title","created_at")
    search_fields = ("title","description")
    list_filter = ("created_at",)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id","owner","email","phone","created_at")
    search_fields = ("email","phone","raw_text")
    list_filter = ("created_at",)

@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ("id","resume","job","score","created_at")
    list_filter = ("created_at",)
