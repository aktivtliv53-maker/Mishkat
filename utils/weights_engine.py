# ============================
#   Mishkat Weights Engine v1.0
#   (Arabic Morphological Patterns)
# ============================

import re

# -------------------------------------------
# 1) وزن فعيلة — مثل: سكينة، جليلة، عظيمة
# -------------------------------------------

def pattern_fa3eela(w: str):
    # مثال: س ك ي ن ة → سكن
    if len(w) == 5 and w[2] == "ي" and w[-1] in ["ة", "ه"]:
        return w[0] + w[1] + w[3]
    return None


# -------------------------------------------
# 2) وزن فعيل — مثل: كريم، عليم، حكيم
# -------------------------------------------

def pattern_fa3eel(w: str):
    # مثال: ك ر ي م → كرم
    if len(w) == 4 and w[2] == "ي":
        return w[0] + w[1] + w[3]
    return None


# -------------------------------------------
# 3) وزن فعّال — مثل: غفّار، توّاب
# -------------------------------------------

def pattern_fa33aal(w: str):
    # مثال: غ ف ف ا ر → غفر
    if len(w) >= 4 and w[1] == w[2]:
        return w[0] + w[1] + w[-1]
    return None


# -------------------------------------------
# 4) وزن مفعول — مثل: مكتوب، مخلوق
# -------------------------------------------

def pattern_maf3ool(w: str):
    # مثال: م ك ت و ب → كتب
    if len(w) >= 5 and w[0] == "م" and "و" in w:
        core = w[1:].replace("و", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 5) وزن تفعيل — مثل: تقديس، تبشير
# -------------------------------------------

def pattern_taf3eel(w: str):
    # مثال: ت ق د ي س → قدس
    if len(w) >= 5 and w[0] == "ت" and "ي" in w:
        core = w[1:].replace("ي", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 6) وزن استفعال — مثل: استغفار، استقامة
# -------------------------------------------

def pattern_istif3aal(w: str):
    # مثال: ا س ت غ ف ا ر → غفر
    if w.startswith("است") and len(w) >= 6:
        core = w[3:].replace("ا", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 7) وزن افتعال — مثل: اختيار، اجتماع
# -------------------------------------------

def pattern_ifti3aal(w: str):
    # مثال: ا خ ت ي ا ر → خير
    if w.startswith("ا") and "ت" in w:
        core = w.replace("ا", "").replace("ت", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 8) وزن انفعال — مثل: انطلاق، انكسار
# -------------------------------------------

def pattern_infi3aal(w: str):
    if w.startswith("ان") and len(w) >= 5:
        core = w[2:].replace("ا", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 9) وزن تفاعل — مثل: تعاون، تناصر
# -------------------------------------------

def pattern_tafaa3ul(w: str):
    if w.startswith("ت") and "ا" in w:
        core = w.replace("ت", "").replace("ا", "")
        if len(core) >= 3:
            return core[:3]
    return None


# -------------------------------------------
# 10) الواجهة الموحدة
# -------------------------------------------

PATTERNS = [
    pattern_fa3eela,
    pattern_fa3eel,
    pattern_fa33aal,
    pattern_maf3ool,
    pattern_taf3eel,
    pattern_istif3aal,
    pattern_ifti3aal,
    pattern_infi3aal,
    pattern_tafaa3ul,
]


def normalize_by_weight(w: str) -> str:
    """
    يمر على جميع الأوزان ويعيد الجذر إن وجد.
    """
    for p in PATTERNS:
        r = p(w)
        if r:
            return r
    return w
