# ============================
#   Mishkat Root Engine v6.0
#   (Corrected Weight Order)
# ============================

import re
from utils.weights_engine import normalize_by_weight


# -------------------------------------------
# 1) تنظيف الكلمة (بدون حذف التاء المربوطة)
# -------------------------------------------

def clean_basic(w: str) -> str:
    w = w.strip()
    w = re.sub(r"[^\u0621-\u064A]", "", w)
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
    # 1) تنظيف أولي بدون حذف التاء المربوطة
    w = clean_basic(w)

    # 2) *** طبقة الأوزان قبل أي تعديل ***
    w = normalize_by_weight(w)

    # 3) الآن نحذف التاء المربوطة بعد تطبيق الوزن
    w = w.replace("ة", "ه")

    # 4) إزالة حروف الزيادة
    w = remove_extra_letters(w)

    # 5) إذا أصبحت 3 أحرف → هذا هو الجذر
    if len(w) == 3:
        return w

    # 6) معالجة الكلمات ذات 4 أحرف
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

    # 7) fallback: أول 3 أحرف
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
