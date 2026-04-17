# utils/comparison_engine.py — v11.3 (Comparative Engine v4)

from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root

def compare_texts_v4(t1, t2):
    a1 = analyze_text_v5(t1)
    a2 = analyze_text_v5(t2)

    r1 = {canonize_root(r): c for r, c in a1["root_frequency"]}
    r2 = {canonize_root(r): c for r, c in a2["root_frequency"]}

    shared = set(r1.keys()) & set(r2.keys())
    unique_1 = set(r1.keys()) - set(r2.keys())
    unique_2 = set(r2.keys()) - set(r1.keys())

    similarity = len(shared) / max(1, len(set(r1.keys()) | set(r2.keys())))

    return {
        "shared_roots": list(shared),
        "unique_1": list(unique_1),
        "unique_2": list(unique_2),
        "similarity": similarity,
        "status": "Comparative Engine v4"
    }