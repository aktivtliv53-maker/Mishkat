# ============================
#   Root Engine v7.3 — Safe Version
#   (اسم الملف root_engine_v7.py كما طلبت)
# ============================

import re
from collections import Counter
from utils.lexicon_v7 import SOVEREIGN_LEXICON, PREFIXES, SUFFIXES, normalize_token

# ------------------------------------
# 1) تنظيف الكلمة
# ------------------------------------
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

# ------------------------------------
# 2) استخراج الجذر
# ------------------------------------
def extract_root_v7(word):
    w = normalize_token(word)
    n = len(w)

    # قاموس سيادي
    if w in SOVEREIGN_LEXICON:
        return SOVEREIGN_LEXICON[w]

    # وزن فعّال (قتال، كتاب)
    if n == 4 and w[1] == "ت":
        return w[0] + w[2] + w[3]

    # وزن فعول (رسول، غفور)
    if n >= 4 and w[-2] == "و":
        if n >= 4:
            return w[0] + w[1] + w[-1]

    # وزن فعيل (عليم، حكيم)
    if n >= 4 and w[-2] == "ي":
        if n >= 4:
            return w[0] + w[1] + w[-1]

    # وزن استفعل (استغفر)
    if w.startswith("است") and n >= 6:
        return w[3] + w[4] + w[5]

    # وزن مفاعلة (مجادلة)
    if w.startswith("م") and n >= 5 and "ا" in w[1:3]:
        return w[1] + w[3] + w[4]

    # fallback
    if n == 3:
        return w
    if n > 3:
        return w[:3]

    return None

# ------------------------------------
# 3) تحليل النص
# ------------------------------------
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
        "status": "Root Engine v7.3 — Safe"
    }
