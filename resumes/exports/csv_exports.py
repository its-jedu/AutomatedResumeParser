import csv, io
from django.http import HttpResponse

def build_match_csv_response(match):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Match ID","Resume ID","Job ID","Score","Cosine","Keyword Ratio","Hits","Missing"])
    d = match.details or {}
    writer.writerow([
        match.id, match.resume_id, match.job_id, d.get("score"),
        d.get("cosine"), d.get("keyword_ratio"),
        ";".join(d.get("keyword_hits", [])),
        ";".join(d.get("keyword_missing", [])),
    ])
    resp = HttpResponse(buf.getvalue(), content_type="text/csv")
    resp["Content-Disposition"] = f'attachment; filename="match_{match.id}.csv"'
    return resp
