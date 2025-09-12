from collections import Counter
import re

try:
    import spacy
    _HAS_SPACY = True
except Exception:
    spacy = None
    _HAS_SPACY = False

_NLP = None
def get_nlp():
    global _NLP
    if _NLP is None and _HAS_SPACY:
        try:
            _NLP = spacy.load("en_core_web_sm")
        except Exception:
            _NLP = None
    return _NLP

BASIC_SKILL_HINTS = {
    "python","django","rest","drf","postgres","postgresql","mysql","selenium","pytest","docker",
    "aws","git","linux","pandas","numpy","ml","nlp","spacy","celery","redis","kafka"
}

def extract_keywords(text: str, max_k=30):
    if not text:
        return []
    nlp = get_nlp()
    tokens = []
    if nlp:
        doc = nlp(text.lower())
        for t in doc:
            if t.is_stop or t.is_punct or len(t.text) < 2:
                continue
            if t.pos_ in {"NOUN","PROPN","VERB","ADJ"}:
                tokens.append(t.lemma_)
    else:
        tokens = re.findall(r"[a-zA-Z]{2,}", text.lower())
    common = Counter(tokens).most_common(max_k)
    return [w for w,_ in common]

def extract_skills(text: str):
    toks = set(extract_keywords(text, max_k=200))
    return sorted(toks.intersection(BASIC_SKILL_HINTS))
