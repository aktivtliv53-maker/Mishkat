# ============================
#   Root Engine v7.0 — نسخة مبسطة للاختبار
# ============================

import re
from collections import Counter
from utils.root_canonizer import canonize_root

STOPWORDS = {
    "من", "في", "على", "عن", "إلى", "و", "يا", "ما", "هذا", "هذه",
    "ذلك", "تلك", "ثم", "ف", "ب", "ل", "ك", "إن", "أن", "قد", "هل",
    "أ", "إ", "ألا", "أفلا", "أولم", "ألم", "لعل", "ليت", "هو", "هي",
    "هم", "هن", "نحن", "أنت", "أنتم", "أنتن"
}

def normalize_text(text):
    text = re.sub(r"[^\u0600-\u06FF\s]", "", text)
    return text.strip()

def extract_words(text):
    text = normalize_text(text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def analyze_text_v7(text):
    """نسخة مبسطة - تستخرج أول 3 أحرف كجذر"""
    words = extract_words(text)
    root_counter = Counter()
    
    for word in words:
        if len(word) >= 3:
            root = word[:3]
            canonical = canonize_root(root)
            if canonical and len(canonical) >= 2:
                root_counter[canonical] += 1
    
    sorted_roots = list(root_counter.most_common())
    
    return {
        "root_frequency": sorted_roots,
        "total_roots": len(sorted_roots),
        "status": "Root Engine v7.0 - Simplified"
    }

# للتوافق
analyze_text_v6 = analyze_text_v7
