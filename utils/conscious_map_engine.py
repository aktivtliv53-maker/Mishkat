# ============================
#   Conscious Map Engine v3.1 — Final
# ============================

from utils.root_engine_v7 import analyze_text_v7
from collections import Counter

STOP_ROOTS = {
    "ال","لا","يا","ثم","كل","كم","هم","هو","هي","هن","به","بم","لك","وب",
    "يت","يش","يك","لع","قد","تك","جا","مو","اس","لن","لم","مع","بل","وت","ور",
    "يو","ين","تر","ير","وق","وع","وه","شي"
}

def is_valid_root(root):
    if not root:
        return False
    if len(root) < 3:
        return False
    if root in STOP_ROOTS:
        return False
    return True

def build_conscious_map(quran, surah_number):
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
        "status": "Conscious Map Engine v3.1 — Filtered"
    }
