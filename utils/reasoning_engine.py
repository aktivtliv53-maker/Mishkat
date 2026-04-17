# utils/reasoning_engine.py — v11.3 (Reasoning Engine v4)

from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root

def build_reasoning_path_v4(quran, query):
    q_analysis = analyze_text_v5(query)
    q_roots = {canonize_root(r): c for r, c in q_analysis["root_frequency"]}

    matches = []

    for ay in quran:
        a_analysis = analyze_text_v5(ay["text"])
        a_roots = {canonize_root(r): c for r, c in a_analysis["root_frequency"]}

        shared = set(q_roots.keys()) & set(a_roots.keys())
        score = len(shared)

        if score > 0:
            matches.append((score, ay, list(shared)))

    matches = sorted(matches, key=lambda x: x[0], reverse=True)

    return {
        "query_roots": list(q_roots.keys()),
        "matches": [
            {
                "ayah": m[1],
                "shared_roots": m[2],
                "score": m[0]
            }
            for m in matches[:20]
        ],
        "status": "Reasoning Engine v4"
    }