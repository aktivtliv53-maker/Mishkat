# ============================
#   Root Canonizer v6.6 — Final
# ============================

import re

# خريطة تصحيح الجذور الخاصة (سورة الفاتحة + جذور شائعة)
SPECIAL_MAP = {
    "لهه": "اله",
    "عال": "علو",
    "ايك": "أيّ",
    "واي": "أيّ",
    "نست": "عون",
    "ذوو": "ذي",
    "انع": "نعم",
}

def remove_tashkeel(text):
    return re.sub(r"[ًٌٍَُِّْـ]", "", text)

def normalize_alef(text):
    return re.sub(r"[إأآا]", "ا", text)

def canonize_root(root):
    r = remove_tashkeel(root)
    r = normalize_alef(r)

    # خريطة التصحيح الخاصة
    if r in SPECIAL_MAP:
        return SPECIAL_MAP[r]

    return r
