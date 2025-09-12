from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from textwrap import wrap

def build_match_pdf_response(match):
    resp = HttpResponse(content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="match_{match.id}.pdf"'
    c = canvas.Canvas(resp, pagesize=A4)
    w, h = A4
    y = h - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Match Report #{match.id}")
    y -= 24
    c.setFont("Helvetica", 11)

    details = match.details or {}
    lines = [
        f"Resume ID: {match.resume_id}",
        f"Job ID: {match.job_id}",
        f"Score: {details.get('score')}%",
        f"Cosine Similarity: {details.get('cosine')}",
        f"Keyword Ratio: {details.get('keyword_ratio')}",
        f"Keyword Hits: {', '.join(details.get('keyword_hits', []))}",
        f"Missing Keywords: {', '.join(details.get('keyword_missing', []))}",
    ]
    for ln in lines:
        for wrapped in wrap(ln, 95):
            c.drawString(50, y, wrapped)
            y -= 16
            if y < 70:
                c.showPage()
                y = h - 50
    c.showPage()
    c.save()
    return resp
