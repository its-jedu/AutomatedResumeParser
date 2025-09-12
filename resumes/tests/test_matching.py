from resumes.services.matching import compute_match

def test_compute_match_scores_reasonably():
    resume = "Experienced Django & DRF developer, Selenium tests, PostgreSQL."
    job = "Looking for a Django REST Framework backend engineer with Selenium and PostgreSQL."
    details = compute_match(
        resume_text=resume,
        job_description=job,
        resume_skills=["django","drf","selenium","postgresql"],
        job_keywords=["django","rest","selenium","postgresql"],
    )
    assert 0 <= details["score"] <= 100
    assert details["cosine"] > 0.1
    assert "django" in details["keyword_hits"]
