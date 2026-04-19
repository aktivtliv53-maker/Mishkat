# ============================
#   Root Engine v7.2 — Final
# ============================

import re
from collections import Counter
from utils.lexicon_v7 import SOVEREIGN_LEXICON, PREFIXES, SUFFIXES, normalize_token

def clean_word(word):
    w = re.sub(r"[^\u0621-\u064A]", "", word)
    w = normalize_token(w)

    for p in sorted(PREFIXES, key=len, reverse=True):
        if w.startswith(p) and len(w) > len(p) + 1:
            w = w[len(p):]
            break

    for s in sorted(SUFFIXES, key=len, reverse=True):
        if w.endswith(s) and len(w) > len(s) + 1:
            w = w[:-len(s)]
            break

    return w

def extract_root_v7(word):
    w = normalize_token(word)
    n = len(w)

    if w in SOVEREIGN_LEXICON:
        return SOVEREIGN_LEXICON[w]

    if n == 4 and w[1] == "ت":
        return w[0] + w[2] + w[3]

    if n == 4 and w[-2] == "و":
        return w[0] + w[1] + w[3]

    if n == 4 and w[-2] == "ي":
        return w[0] + w[1] + w[3]

    if w.startswith("است") and n >= 6:
        return w[3] + w[4] + w[5]

    if w.startswith("م") and "ا" in w[1:3]:
        return w[1] + w[3] + w[4]

    if n == 3:
        return w
    if n > 3:
        return w[:3]

    return None

def analyze_text_v7(text):
    words = text.split()
    roots = []

    for w in words:
        cleaned = clean_word(w)
        if not cleaned:
            continue

        root = extract_root_v7(cleaned)
        if root:
            roots.append(root)

    freq = Counter(roots).most_common()
    return {
        "root_frequency": freq,
        "total_roots": len(roots),
        "status": "Root Engine v7.2"
    }
