from resumes.services.parsing import simple_extract_entities

def test_simple_extract_entities():
    text = "Email me at test.user@example.com or call +234 801-234-5678"
    email, phone = simple_extract_entities(text)
    assert "test.user@" in email
    assert "+234" in phone
