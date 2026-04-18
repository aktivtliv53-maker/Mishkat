# ============================
#   Mishkat Root Engine v6.5
#   (Canonical Triliteral Extraction)
# ============================

import re
from utils.weights_engine import normalize_by_weight

# -------------------------------------------
# 1) تنظيف الكلمة
# -------------------------------------------

def clean_word(w: str) -> str:
    w = w.strip()
    w = re.sub(r"[^\u0621-\u064A]", "", w)
    w = w.replace("أ","ا").replace("إ","ا").replace("آ","ا")
    w = w.replace("ة","ه")
    return w

# -------------------------------------------
# 2) إزالة أل التعريف
# -------------------------------------------

def remove_al(w: str) -> str:
    if w.startswith("ال") and len(w) > 3:
        return w[2:]
    return w

# -------------------------------------------
# 3) إزالة الضمائر
# -------------------------------------------

PRONOUN_SUFFIXES = ["ه","هم","هن","كما","كم","نا","ي","ك"]

def remove_pronouns(w: str) -> str:
    for suf in PRONOUN_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf)+2:
            return w[:-len(suf)]
    return w

# -------------------------------------------
# 4) إزالة حروف الزيادة
# -------------------------------------------

EXTRA = set("سألتومنيها")

def remove_extra(w: str) -> str:
    if len(w) > 3:
        return "".join([c for c in w if c not in EXTRA])
    return w

# -------------------------------------------
# 5) معالجة الأوزان الصرفية
# -------------------------------------------

def apply_patterns(w: str) -> str:
    # فاعل → ملك
    if len(w) == 4 and w[1] == "ا":
        return w[0] + w[2] + w[3]

    # فعيل → دين
    if len(w) == 4 and w[2] == "ي":
        return w[0] + w[1] + w[3]

    # نفعل → نعبد → عبد
    if len(w) == 4 and w[0] == "ن":
        return w[1:]

    return w

# -------------------------------------------
# 6) استخراج الجذر
# -------------------------------------------

def extract_root(w: str) -> str:
    w = clean_word(w)
    w = remove_al(w)
    w = remove_pronouns(w)

    w = normalize_by_weight(w)
    w = apply_patterns(w)
    w = remove_extra(w)

    # إذا أصبح 3 أحرف → هذا هو الجذر
    if len(w) == 3:
        return w

    # معالجة 4 أحرف
    if len(w) == 4:
        for c in ["ا","و","ي"]:
            if c in w:
                w2 = w.replace(c,"")
                if len(w2) == 3:
                    return w2

    # لا نستخدم fallback الخاطئ
    return w[:3]

# -------------------------------------------
# 7) الواجهة الرئيسية
# -------------------------------------------

def analyze_text_v6(text: str):
    words = text.split()
    roots = []

    for w in words:
        r = extract_root(w)
        roots.append(r)

    freq = {}
    for r in roots:
        freq[r] = freq.get(r, 0) + 1

    return {
        "roots": roots,
        "root_frequency": list(freq.items())
    }
