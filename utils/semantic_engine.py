# utils/semantic_engine.py — v12
# Semantic Engine now uses:
# Root Engine v6  +  Root Canonizer v1

from utils.root_engine import extract_root, analyze_text_v5
from utils.root_canonizer import canonize_root

import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def extract_roots_from_text(text: str):
    text = clean_text(text)
    words = text.split()

    roots = []
    for w in words:
        raw = extract_root(w)
        canon = canonize_root(raw)
        if canon:
            roots.append(canon)

    return roots

def analyze_word(text: str):
    info = analyze_text_v5(text)
    info["canonical_root"] = canonize_root(info["roots"][0])
    return info
