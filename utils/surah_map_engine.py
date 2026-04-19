# utils/surah_map_engine.py
# ============================
#   Surah Map Engine v7
#   مبني على Root Engine v7 (pattern-based)
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root

def get_surah_text(quran, surah_number):
    """
    تجميع نص السورة كاملة في سطر واحد
    quran: قائمة الآيات، كل عنصر dict يحتوي على:
        - "surah_number"
        - "text"
    """
    return " ".join(
        a["text"] for a in quran
        if a.get("surah_number") == surah_number
    )

def get_surah_roots_v7(quran, surah_number):
    """
    إرجاع تكرار الجذور في سورة معينة باستخدام Root Engine v7
    """
    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v7(text)

    freq = {}
    for root, count in analysis["root_frequency"]:
        canon = canonize_root(root)
        if not canon:
            continue
        freq[canon] = freq.get(canon, 0) + count

    freq_sorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return freq_sorted

def get_surah_stats_v7(quran, surah_number):
    """
    إحصائيات السورة:
    - عدد الجذور الفريدة
    - قائمة تكرار الجذور
    - أعلى 20 جذرًا
    """
    roots = get_surah_roots_v7(quran, surah_number)
    return {
        "surah": surah_number,
        "unique_roots": len(roots),
        "root_frequency": roots,
        "top_roots": roots[:20],
        "status": "Surah Map v7 — pattern-based roots"
    }

def get_surah_signature_v7(quran, surah_number, top_n=10):
    """
    البصمة الجذرية للسورة: أعلى N جذور
    """
    return get_surah_roots_v7(quran, surah_number)[:top_n]

def get_surah_links_v7(quran, surah_number):
    """
    الروابط بين السور بناءً على الجذور المشتركة:
    - لكل سورة أخرى: عدد الجذور المشتركة
    """
    roots_s = dict(get_surah_roots_v7(quran, surah_number))
    surahs = sorted(set(a["surah_number"] for a in quran))

    links = []

    for s in surahs:
        if s == surah_number:
            continue

        roots_other = dict(get_surah_roots_v7(quran, s))
        shared = set(roots_s.keys()) & set(roots_other.keys())

        if shared:
            links.append({
                "surah": s,
                "shared_roots": list(shared),
                "weight": len(shared)
            })

    links = sorted(links, key=lambda x: x["weight"], reverse=True)
    return links
