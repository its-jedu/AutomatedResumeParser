from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ResumeViewSet, MatchViewSet

router = DefaultRouter()
router.register("jobs", JobViewSet, basename="job")
router.register("resumes", ResumeViewSet, basename="resume")

match_list = MatchViewSet.as_view({"post": "create"})
match_export_csv = MatchViewSet.as_view({"get": "export_csv"})
match_export_pdf = MatchViewSet.as_view({"get": "export_pdf"})

urlpatterns = [
    path("", include(router.urls)),
    path("match/", match_list, name="match"),
    path("match/<int:pk>/export/csv/", match_export_csv, name="match-export-csv"),
    path("match/<int:pk>/export/pdf/", match_export_pdf, name="match-export-pdf"),
]
