from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Resume, Job, MatchResult
from .serializers import JobSerializer, ResumeUploadSerializer, ResumeDetailSerializer, MatchResultSerializer
from .permissions import IsOwnerOrReadOnly
from .services.parsing import extract_text, simple_extract_entities
from .services.nlp import extract_skills, extract_keywords
from .services.matching import compute_match
from .exports.csv_exports import build_match_csv_response
from .exports.pdf_exports import build_match_pdf_response

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def keywords(self, request):
        desc = request.data.get("description","")
        kws = extract_keywords(desc, max_k=30)
        return Response({"keywords": kws})

class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Resume.objects.filter(owner=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action in {"create","update","partial_update"}:
            return ResumeUploadSerializer
        return ResumeDetailSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        s = ResumeUploadSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        resume: Resume = s.save(owner=request.user)

        text = extract_text(resume.file.path)
        resume.raw_text = text[:2_000_000]
        email, phone = simple_extract_entities(text)
        resume.email = email or ""
        resume.phone = phone or ""
        resume.skills = extract_skills(text)
        resume.save(update_fields=["raw_text","email","phone","skills"])

        return Response(ResumeDetailSerializer(resume).data, status=status.HTTP_201_CREATED)

class MatchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        POST /api/match/
        body: {resume_id: int, job_id: int} OR {resume_text: str, job_text: str}
        """
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")
        resume_text = request.data.get("resume_text")
        job_text = request.data.get("job_text")

        if resume_id and job_id:
            try:
                resume = Resume.objects.get(id=resume_id, owner=request.user)
            except Resume.DoesNotExist:
                return Response({"detail":"Resume not found."}, status=404)
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                return Response({"detail":"Job not found."}, status=404)

            details = compute_match(
                resume_text=resume.raw_text,
                job_description=job.description,
                resume_skills=resume.skills,
                job_keywords=job.keywords,
            )
            match = MatchResult.objects.create(resume=resume, job=job, score=details["score"], details=details)
            return Response(MatchResultSerializer(match).data, status=200)

        if resume_text and job_text:
            details = compute_match(
                resume_text=resume_text,
                job_description=job_text,
                resume_skills=extract_skills(resume_text),
                job_keywords=extract_keywords(job_text, 30),
            )
            return Response({"score": details["score"], "details": details}, status=200)

        return Response({"detail":"Provide (resume_id & job_id) or (resume_text & job_text)."}, status=400)

    @action(detail=True, methods=["get"], url_path="export/csv")
    def export_csv(self, request, pk=None):
        try:
            m = MatchResult.objects.get(id=pk, resume__owner=request.user)
        except MatchResult.DoesNotExist:
            return Response({"detail":"Not found."}, status=404)
        return build_match_csv_response(m)

    @action(detail=True, methods=["get"], url_path="export/pdf")
    def export_pdf(self, request, pk=None):
        try:
            m = MatchResult.objects.get(id=pk, resume__owner=request.user)
        except MatchResult.DoesNotExist:
            return Response({"detail":"Not found."}, status=404)
        return build_match_pdf_response(m)
