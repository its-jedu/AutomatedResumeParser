import io
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def client(db):
    u = User.objects.create_user(username="julius", password="pass12345")
    c = APIClient()
    tokens = c.post(reverse("token_obtain_pair"), {"username":"julius","password":"pass12345"}, format="json").json()
    c.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    return c

def test_resume_upload_and_match(client):
    # Create job
    job = client.post("/api/jobs/", {
        "title":"Backend Dev",
        "description":"Django, DRF, Selenium, PostgreSQL",
        "keywords":["django","drf","selenium","postgresql"]
    }, format="json").json()

    # Upload a plain-text resume file
    f = io.BytesIO(b"Senior Django and DRF engineer. Selenium automation. PostgreSQL.")
    f.name = "cv.txt"
    resume = client.post("/api/resumes/", {"file": f}, format="multipart").json()

    # Match
    res = client.post("/api/match/", {"resume_id": resume["id"], "job_id": job["id"]}, format="json")
    assert res.status_code == 200
    assert 0 <= res.json()["score"] <= 100
