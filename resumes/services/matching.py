from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _tfidf_cosine(resume_text: str, job_text: str) -> float:
    vect = TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=1)
    X = vect.fit_transform([job_text or "", resume_text or ""])
    return float(cosine_similarity(X[0], X[1])[0,0])

def _keyword_overlap(resume_tokens: List[str], job_keywords: List[str]) -> Tuple[int,int,float,list,list]:
    resume_set = set(t.lower() for t in (resume_tokens or []))
    job_set = set(k.lower() for k in (job_keywords or []))
    hits = sorted(resume_set.intersection(job_set))
    miss = sorted(job_set - resume_set)
    ratio = (len(hits) / len(job_set)) if job_set else 0.0
    return len(hits), len(job_set), ratio, hits, miss

def compute_match(resume_text: str, job_description: str, resume_skills: List[str], job_keywords: List[str]) -> Dict:
    cosine = _tfidf_cosine(resume_text, job_description)
    _, _, kw_ratio, hits, missing = _keyword_overlap(resume_skills, job_keywords)
    score = round((0.7 * cosine + 0.3 * kw_ratio) * 100, 2)
    return {
        "score": score,
        "cosine": round(cosine, 4),
        "keyword_ratio": round(kw_ratio, 4),
        "keyword_hits": hits,
        "keyword_missing": missing,
    }
