# utils/position_engine.py — v11
# Position Engine v3 — محرك المواقع المتقدم

import re

# ============================================================
# 1) تحليل مواقع الحروف داخل الكلمة
# ============================================================
def analyze_letter_positions(word: str):
    """
    يعيد:
    - كل حرف
    - موقعه
    - نوع الموقع (بداية / وسط / نهاية)
    """

    word = word.strip()
    letters = list(word)

    results = []

    for i, ch in enumerate(letters):
        if i == 0:
            pos = "بداية"
        elif i == len(letters) - 1:
            pos = "نهاية"
        else:
            pos = "وسط"

        results.append({
            "letter": ch,
            "index": i + 1,
            "position": pos
        })

    return results

# ============================================================
# 2) استخراج الجذر البنيوي (Structural Root Guess)
# ============================================================
def guess_structural_root(word: str):
    """
    محاولة استخراج الجذر بناءً على:
    - مواقع الحروف
    - الحروف الزائدة
    - الأنماط الشائعة
    """

    w = word.strip()

    # إزالة التشكيل
    w = re.sub(r"[ًٌٍَُِّْـ]", "", w)

    # إزالة الألف والواو والياء الزائدة
    for c in ["ا", "و", "ي"]:
        if len(w) > 3 and c in w:
            w2 = w.replace(c, "")
            if len(w2) == 3:
                return w2

    # fallback
    return w[:3] if len(w) >= 3 else w

# ============================================================
# 3) تحليل مواقع الجذر داخل الكلمة
# ============================================================
def analyze_root_positions(word: str):
    """
    يعيد:
    - الجذر المتوقع
    - مواقع حروف الجذر داخل الكلمة
    """

    root = guess_structural_root(word)
    positions = []

    for r in root:
        idx = word.find(r)
        if idx != -1:
            positions.append({
                "root_letter": r,
                "index": idx + 1
            })

    return {
        "root": root,
        "positions": positions
    }

# ============================================================
# 4) Position Engine v3 — التحليل الكامل
# ============================================================
def analyze_word_positions_v3(word: str):
    """
    التحليل الكامل للكلمة:
    - مواقع الحروف
    - الجذر البنيوي
    - مواقع الجذر
    - شكل الكلمة
    """

    letters = analyze_letter_positions(word)
    root_info = analyze_root_positions(word)

    shape = f"{len(word)}-letter word"

    return {
        "word": word,
        "shape": shape,
        "letters": letters,
        "root": root_info["root"],
        "root_positions": root_info["positions"],
        "status": "Position Engine v3 analysis complete"
    }