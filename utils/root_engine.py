# ============================
#   Mishkat Root Engine v4.0
#   (Correct Arabic Root Extraction)
# ============================

import re

# ----------------------------
# 1) تنظيف الكلمة قبل التحليل
# ----------------------------

def clean_word(w: str) -> str:
    w = w.strip()
    w = re.sub(r"[^\u0621-\u064A]", "", w)  # إزالة أي شيء غير حرف عربي
    w = w.replace("ة", "ه")  # توحيد التاء المربوطة
    return w


# -------------------------------------------
# 2) معالجة وزن (فَعِيلَة) مثل: سكينة → سكن
# -------------------------------------------

def normalize_pattern_fa3eela(w: str) -> str:
    """
    إذا كانت الكلمة على وزن (فَعِيلَة):
    حرف + حرف + ي + حرف + ة/ه
    نعيد الجذر: الأول + الثاني + الرابع
    """
    if len(w) == 5:
        if w[2] == "ي" and w[-1] in ["ه", "ة"]:
            return w[0] + w[1] + w[3]
    return w


# -------------------------------------------------
# 3) إزالة حروف الزيادة الشائعة (سألتمونيها)
# -------------------------------------------------

EXTRA_LETTERS = set("سألتومنيها")

def remove_extra_letters(w: str) -> str:
    # نزيل الحروف الزائدة فقط إذا كانت الكلمة أطول من 3
    if len(w) > 3:
        return "".join([c for c in w if c not in EXTRA_LETTERS])
    return w


# -------------------------------------------
# 4) استخراج الجذر الثلاثي بعد التطبيع
# -------------------------------------------

def extract_root(w: str) -> str:
    w = clean_word(w)
    w = normalize_pattern_fa3eela(w)
    w = remove_extra_letters(w)

    # إذا أصبحت الكلمة 3 أحرف → هذا هو الجذر
    if len(w) == 3:
        return w

    # إذا 4 أحرف → نحذف حرف علّة أو تضعيف
    if len(w) == 4:
        # حذف حرف علّة
        for c in ["ا", "و", "ي"]:
            if c in w:
                w2 = w.replace(c, "")
                if len(w2) == 3:
                    return w2

        # حذف تضعيف
        if w[1] == w[2]:
            return w[0] + w[1] + w[3]

    # fallback: نأخذ أول 3 أحرف
    return w[:3]


# -------------------------------------------
# 5) الواجهة الرئيسية للتحليل
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
