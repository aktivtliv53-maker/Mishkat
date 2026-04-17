from utils.root_engine import analyze_text_v5
from utils.ayah_matcher import match_ayahs_by_roots
from utils.root_canonizer import canonize_root


def build_journey(query, quran):

    # =========================
    # 1) تحليل الجذور
    # =========================
    analysis = analyze_text_v5(query)

    roots = [
        canonize_root(r) for r, _ in analysis["root_frequency"]
        if canonize_root(r)
    ]

    # =========================
    # 2) مطابقة الآيات
    # =========================
    matches = match_ayahs_by_roots(roots, quran)

    if not matches:
        return []

    # =========================
    # 3) بناء المسار (5 مراحل)
    # =========================
    journey = []

    labels = [
        "🌱 بداية",
        "🧠 وعي",
        "💡 تعمق",
        "🛡 تثبيت",
        "🌿 رجاء"
    ]

    for i in range(min(5, len(matches))):
        ay = matches[i]

        journey.append({
            "stage": labels[i],
            "surah": ay["surah"],
            "ayah": ay["ayah"],
            "text": ay["text"]
        })

    return journey