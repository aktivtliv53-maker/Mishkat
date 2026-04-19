# ============================
#   Conscious Map Engine v3 — Final
#   Fully Compatible with Root Engine v7
#   No canonize_root, No legacy imports
# ============================

from utils.root_engine_v7 import analyze_text_v7

def build_conscious_map(quran, surah_number):
    """
    بناء الخريطة الوجودية للسورة:
    - استخراج الجذور
    - حساب التكرار
    - بناء مستويات الوعي الجذري
    """

    # 1) جمع آيات السورة
    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    all_roots = []

    # 2) استخراج الجذور من كل آية
    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        for root, count in analysis["root_frequency"]:
            all_roots.append(root)

    # 3) حساب التكرار
    from collections import Counter
    freq = Counter(all_roots)

    # 4) بناء مستويات الوعي (بسيطة الآن — يمكن تطويرها لاحقًا)
    levels = []
    for root, count in freq.items():
        levels.append({
            "root": root,
            "weight": count,
            "level": 1 if count == 1 else 2 if count <= 3 else 3
        })

    # 5) ترتيب المستويات
    levels = sorted(levels, key=lambda x: x["weight"], reverse=True)

    return {
        "surah": surah_number,
        "levels": levels,
        "unique_roots": len(freq),
        "status": "Conscious Map Engine v3 — Root Engine v7"
    }
