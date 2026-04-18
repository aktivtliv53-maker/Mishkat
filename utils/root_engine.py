# ============================
#   Root Engine v6.6 — True Root Extraction (Final)
#   Stable Version for Mishkat v13
# ============================

import re
from collections import Counter
from utils.root_canonizer import canonize_root

# كلمات ضعيفة للإزالة
STOPWORDS = {
    "من", "في", "على", "عن", "إلى", "و", "يا", "ما", "هذا", "هذه",
    "ذلك", "تلك", "ثم", "ف", "ب", "ل", "ك", "إن", "أن", "قد", "هل",
    "أ", "إ", "ألا", "أفلا", "أولم", "ألم", "لعل", "ليت", "هو", "هي",
    "هم", "هن", "نحن", "أنت", "أنتم", "أنتن"
}

def normalize_text(text):
    """تطبيع النص وإزالة الرموز غير العربية"""
    text = re.sub(r"[^\u0600-\u06FF\s]", "", text)
    return text.strip()

def extract_words(text):
    """استخراج الكلمات من النص مع إزالة الكلمات الضعيفة"""
    text = normalize_text(text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 1]

def extract_root(word):
    """استخراج الجذر الثلاثي الحقيقي بدون حذف زائد"""

    w = word

    # إزالة التشكيل
    w = re.sub(r"[ًٌٍَُِّْـ]", "", w)

    # إزالة أل التعريف
    if w.startswith("ال"):
        w = w[2:]

    # قائمة حروف الزيادة الصحيحة (سألتمونيها)
    EXTRA = set("سألتومنيها")

    # إذا الكلمة 3 أحرف → هذا هو الجذر
    if len(w) == 3:
        return w

    # إذا الكلمة 4 أحرف → نحاول حذف حرف زيادة واحد فقط
    if len(w) == 4:
        # 1) حذف حرف زيادة واحد فقط
        for c in EXTRA:
            if c in w:
                t = w.replace(c, "", 1)
                if len(t) == 3:
                    return t

        # 2) حذف حرف علة واحد فقط
        for c in ["ا", "و", "ي"]:
            if c in w:
                t = w.replace(c, "", 1)
                if len(t) == 3:
                    return t

    # fallback آمن: لا نسمح بجذور ثنائية
    if len(w) >= 3:
        return w[:3]

    return w

def analyze_text_v6(text):
    """Root Engine v6.6 — استخراج جذور ثلاثية حقيقية"""
    words = extract_words(text)
    root_counter = Counter()

    for word in words:
        root = extract_root(word)
        canonical = canonize_root(root)

        # الجذر يجب أن يكون ثلاثيًا فقط
        if canonical and len(canonical) == 3:
            root_counter[canonical] += 1

    return {
        "root_frequency": list(root_counter.most_common()),
        "status": "Root Engine v6.6 — True Root Extraction"
    }

# للتوافق مع الإصدارات القديمة
analyze_text_v4 = analyze_text_v6
analyze_text_v5 = analyze_text_v6
