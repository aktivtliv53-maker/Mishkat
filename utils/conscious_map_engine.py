# ============================
#   Conscious Map Engine v4 — Sovereign Edition
#   (اسم الملف ثابت كما طلبت)
#   يعمل على كل سور القرآن
# ============================

from collections import Counter
from utils.root_engine_v7 import analyze_text_v7
from utils.root_filter_v1 import is_valid_root
from utils.lexicon_v7_extended import SOVEREIGN_LEXICON_EXTENDED
from utils.lexicon_v7 import normalize_token

# ------------------------------------
# 1) تطبيع الجذر عبر القاموس الموسّع
# ------------------------------------
def normalize_root(root):
    r = normalize_token(root)
    if r in SOVEREIGN_LEXICON_EXTENDED:
        return SOVEREIGN_LEXICON_EXTENDED[r]
    return r

# ------------------------------------
# 2) بناء الخريطة الوجودية
# ------------------------------------
def build_conscious_map(quran, surah_number):
    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    all_roots = []

    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])

        for root, count in analysis["root_frequency"]:
            root = normalize_root(root)

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
        "status": "Conscious Map v4 — Sovereign Filtering + Extended Lexicon"
    }
