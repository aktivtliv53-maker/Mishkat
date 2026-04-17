import json
from final_finder_v2 import normalize

def load_roots(path="data/roots_index.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

ROOTS_DATA = load_roots()

def get_root_entry(root):
    root_norm = normalize(root)
    for entry in ROOTS_DATA:
        if normalize(entry.get("root", "")) == root_norm:
            return entry
    return None

def compute_semantic_diversity(root_entry):
    """
    تنوّع دلالي تقريبي:
    - نجمع الكلمات في الآيات
    - نحسب عدد الكلمات المميزة
    - نحسب نسبة التنوع = عدد الكلمات المميزة / إجمالي الكلمات
    """
    if not root_entry:
        return 0.0, 0, 0

    ayahs = root_entry.get("ayahs", [])
    total_words = 0
    unique_words = set()

    for a in ayahs:
        text = a.get("text", "")
        for w in text.split():
            w_norm = normalize(w)
            if len(w_norm) <= 2:
                continue
            total_words += 1
            unique_words.add(w_norm)

    if total_words == 0:
        return 0.0, 0, 0

    diversity_ratio = len(unique_words) / total_words
    return diversity_ratio, len(unique_words), total_words

def get_root_semantic_diversity(root):
    entry = get_root_entry(root)
    return compute_semantic_diversity(entry)