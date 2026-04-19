# ============================
#   Conscious Map Engine v4
#   Root → Field → Meaning
# ============================

from utils.root_engine_v7_2 import analyze_text_v7_2
from collections import Counter

FIELDS = {
    "قوم": ("الحركة", "القيام – النهضة – الفعل"),
    "علو": ("العلو", "الارتفاع – السيطرة – الهيمنة"),
    "ربب": ("الربوبية", "الرعاية – التربية – الإحاطة"),
    "قول": ("البيان", "الكلام – الخطاب – الوحي"),
    "رحم": ("الرحمة", "اللطف – العطاء – الرعاية"),
    "خير": ("القيم", "المنفعة – الصلاح – البر"),
    "دين": ("المنهج", "الطاعة – النظام – الشريعة"),
    "كون": ("الوجود", "الخلق – التكوين – التحول"),
    "بين": ("الوضوح", "التمييز – البيان – الإظهار"),
    "صرط": ("الهداية", "الطريق – الاتجاه – الاستقامة"),
}

def build_conscious_map_v4(quran, surah_number):
    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    all_roots = []

    for ayah in ayahs:
        analysis = analyze_text_v7_2(ayah["text"])
        for root, count in analysis["root_frequency"]:
            all_roots.append(root)

    freq = Counter(all_roots)

    levels = []
    for root, count in freq.items():
        field, meaning = FIELDS.get(root, ("غير مصنف", "—"))
        levels.append({
            "root": root,
            "weight": count,
            "level": 1 if count == 1 else 2 if count <= 3 else 3,
            "field": field,
            "meaning": meaning
        })

    levels = sorted(levels, key=lambda x: x["weight"], reverse=True)

    return {
        "surah": surah_number,
        "levels": levels,
        "unique_roots": len(freq),
        "status": "Conscious Map v4 — Root–Field–Meaning"
    }
