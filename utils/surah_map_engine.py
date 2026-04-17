# utils/surah_map_engine.py — v11.3 (Surah Map v5)

from utils.semantic_engine import extract_roots_from_text
from utils.root_canonizer import canonize_root
from utils.root_engine import analyze_text_v5

def get_surah_text(quran, surah_number):
    return " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])

def get_surah_roots_v5(quran, surah_number):
    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v5(text)

    freq = {}
    for root, count in analysis["root_frequency"]:
        canon = canonize_root(root)
        freq[canon] = freq.get(canon, 0) + count

    freq_sorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return freq_sorted

def get_surah_stats_v5(quran, surah_number):
    roots = get_surah_roots_v5(quran, surah_number)
    return {
        "surah": surah_number,
        "unique_roots": len(roots),
        "root_frequency": roots,
        "top_roots": roots[:20],
        "status": "Surah Map v5 computed"
    }

def get_surah_signature_v5(quran, surah_number):
    return get_surah_roots_v5(quran, surah_number)[:10]

def get_surah_links_v5(quran, surah_number):
    roots_s = dict(get_surah_roots_v5(quran, surah_number))
    surahs = sorted(set(a["surah_number"] for a in quran))

    links = []

    for s in surahs:
        if s == surah_number:
            continue

        roots_other = dict(get_surah_roots_v5(quran, s))
        shared = set(roots_s.keys()) & set(roots_other.keys())

        if shared:
            links.append({
                "surah": s,
                "shared_roots": list(shared),
                "weight": len(shared)
            })

    links = sorted(links, key=lambda x: x["weight"], reverse=True)
    return links