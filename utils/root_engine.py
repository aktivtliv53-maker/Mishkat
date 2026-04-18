# ============================
#   Root Engine v6.6 — True Root Extraction
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
    """استخراج الجذر الثلاثي الحقيقي"""
    w = word

    # إزالة التشكيل
    w = re.sub(r"[ًٌٍَُِّْـ]", "", w)

    # إزالة أل التعريف
    if w.startswith("ال"):
        w = w[2:]

    # إزالة حروف الزيادة
    EXTRA = set("سألتومنيها")
    core = "".join([c for c in w if c not in EXTRA])

    # إذا أصبح 3 أحرف → هذا هو الجذر
    if len(core) == 3:
        return core

    # إذا 4 أحرف → حاول حذف حرف علة
    if len(core) == 4:
        for c in ["ا", "و", "ي"]:
            if c in core:
                t = core.replace(c, "")
                if len(t) == 3:
                    return t

    # fallback: أول 3 أحرف بعد التنظيف (نادرًا ما يحدث)
    return core[:3]

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
