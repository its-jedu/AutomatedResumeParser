from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(fp_path: str) -> str:
    try:
        return pdf_extract_text(fp_path) or ""
    except Exception:
        text = []
        try:
            reader = PdfReader(fp_path)
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        except Exception:
            return ""

def extract_text_from_docx(fp_path: str) -> str:
    doc = Document(fp_path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(fp_path: str) -> str:
    p = fp_path.lower()
    if p.endswith(".pdf"):
        return extract_text_from_pdf(fp_path)
    if p.endswith(".docx"):
        return extract_text_from_docx(fp_path)
    with open(fp_path, "rb") as f:
        return f.read().decode(errors="ignore")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d \-]{8,}\d)")

def simple_extract_entities(text: str):
    email_match = EMAIL_RE.search(text or "")
    phone_match = PHONE_RE.search(text or "")
    email = email_match.group(0) if email_match else None
    phone = phone_match.group(0) if phone_match else None
    return email, phone
