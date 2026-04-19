# ============================
#   Conscious Map Engine v3.1 — Final
#   Fully Compatible with Root Engine v7
#   With Root Filtering (STOPWORDS + Non-roots)
# ============================

from utils.root_engine_v7 import analyze_text_v7
from collections import Counter

# الكلمات التي يجب حذفها من الخريطة الوجودية
STOP_ROOTS = {
    "ال","لا","يا","ثم","كل","كم","هم","هو","هي","هن","هم","به","بم","لك","وب",
    "يت","يش","يك","لع","قد","تك","جا","مو","اس","لن","لم","مع","بل","وت","ور",
    "يو","ين","تر","ير","وق","وع","كم","وه","شي","يت","يش","يك"
}

def is_valid_root(root):
    """فلترة الجذور غير الحقيقية"""
    if not root:
        return False
    if len(root) < 3:
        return False
    if root in STOP_ROOTS:
        return False
    # منع المقاطع التي ليست جذورًا
    if any(char in root for char in ["ا", "و", "ي"]) and len(root) == 3:
        # نسمح فقط إذا كانت جذرًا معروفًا
        return True
    return True

def build_conscious_map(quran, surah_number):
    """بناء الخريطة الوجودية للسورة"""

    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    all_roots = []

    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        for root, count in analysis["root_frequency"]:
            if is_valid_root(root):
                all_roots.append(root)

    freq = Counter(all_roots)

    levels = []
    for root, count in freq.items():
        levels.append({
            "root": root,
            "weight": count,
            "level": 1 if count == 1 else 2 if count <= 3 else 3
        })

    levels = sorted(levels, key=lambda x: x["weight"], reverse=True)

    return {
        "surah": surah_number,
        "levels": levels,
        "unique_roots": len(freq),
        "status": "Conscious Map Engine v3.1 — Filtered Roots"
    }
