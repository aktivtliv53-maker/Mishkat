# ============================
#   Surah Map Engine v7 — Final
#   Fully Compatible with Root Engine v7
#   No canonize_root, No legacy imports
# ============================

from utils.root_engine_v7 import analyze_text_v7

def get_surah_text(quran, surah_number):
    """دمج نصوص السورة في نص واحد"""
    return " ".join(
        a["text"] for a in quran
        if a.get("surah_number") == surah_number
    )

def get_surah_roots_v7(quran, surah_number):
    """إرجاع الجذور مع تكرارها داخل السورة"""
    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v7(text)

    # الجذور جاهزة من v7 ولا تحتاج تطبيع إضافي
    return analysis["root_frequency"]

def get_surah_stats_v7(quran, surah_number):
    """إحصائيات السورة"""
    roots = get_surah_roots_v7(quran, surah_number)

    return {
        "surah": surah_number,
        "unique_roots": len(roots),
        "root_frequency": roots,
        "top_roots": roots[:20],
        "status": "Surah Map v7 — pattern-based roots"
    }

def get_surah_signature_v7(quran, surah_number, top_n=10):
    """البصمة الجذرية للسورة"""
    return get_surah_roots_v7(quran, surah_number)[:top_n]

def get_surah_links_v7(quran, surah_number):
    """العلاقات بين السور بناءً على الجذور المشتركة"""
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
