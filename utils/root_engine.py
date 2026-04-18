# ============================
#   Mishkat Root Engine v5.0
#   (Integrated with Weights Engine)
# ============================

import re
from utils.weights_engine import normalize_by_weight


# -------------------------------------------
# 1) تنظيف الكلمة قبل التحليل
# -------------------------------------------

def clean_word(w: str) -> str:
    w = w.strip()
    w = re.sub(r"[^\u0621-\u064A]", "", w)  # إزالة أي شيء غير حرف عربي
    w = w.replace("ة", "ه")  # توحيد التاء المربوطة
    return w


# -------------------------------------------
# 2) إزالة حروف الزيادة (سألتمونيها)
# -------------------------------------------

EXTRA_LETTERS = set("سألتومنيها")

def remove_extra_letters(w: str) -> str:
    if len(w) > 3:
        return "".join([c for c in w if c not in EXTRA_LETTERS])
    return w


# -------------------------------------------
# 3) استخراج الجذر الثلاثي
# -------------------------------------------

def extract_root(w: str) -> str:
    # تنظيف أولي
    w = clean_word(w)

    # تطبيق طبقة الأوزان
    w = normalize_by_weight(w)

    # إزالة حروف الزيادة
    w = remove_extra_letters(w)

    # إذا أصبحت 3 أحرف → هذا هو الجذر
    if len(w) == 3:
        return w

    # معالجة الكلمات ذات 4 أحرف
    if len(w) == 4:
        # حذف حرف علّة
        for c in ["ا", "و", "ي"]:
            if c in w:
                w2 = w.replace(c, "")
                if len(w2) == 3:
                    return w2

        # حذف التضعيف
        if w[1] == w[2]:
            return w[0] + w[1] + w[3]

    # fallback: أول 3 أحرف
    return w[:3]


# -------------------------------------------
# 4) الواجهة الرئيسية للتحليل
# -------------------------------------------

def analyze_text_v5(text: str):
    words = text.split()
    roots = []

    for w in words:
        r = extract_root(w)
        roots.append(r)

    # حساب التكرار
    freq = {}
    for r in roots:
        freq[r] = freq.get(r, 0) + 1

    root_frequency = [(r, freq[r]) for r in freq]

    return {
        "roots": roots,
        "root_frequency": root_frequency
    }
