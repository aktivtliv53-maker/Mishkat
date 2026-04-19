# utils/root_engine_v7.py

import re
from collections import Counter
from utils.lexicon_v7 import (
    SOVEREIGN_LEXICON,
    PREFIXES,
    SUFFIXES,
    normalize_token,
)
from utils.root_canonizer import canonize_root  # إن أردت التطبيع الوجودي

# يمكن لاحقًا دمج STOPWORDS مع ما عندك في v6.6
STOPWORDS = {
    "من", "في", "على", "عن", "الى", "إلى", "و", "يا", "ما", "هذا", "هذه",
    "ذلك", "تلك", "ثم", "ف", "ب", "ل", "ك", "إن", "أن", "قد", "هل",
    "أ", "إ", "ألا", "أفلا", "أولم", "ألم", "لعل", "ليت", "هو", "هي",
    "هم", "هن", "نحن", "أنت", "أنتم", "أنتن", "ولا"
}

def strip_diacritics(text: str) -> str:
    return re.sub(r"[ًٌٍَُِّْـ]", "", text)

def normalize_arabic(text: str) -> str:
    text = strip_diacritics(text)
    text = re.sub(r"[إأآا]", "ا", text)
    return text

def clean_word(raw: str) -> str:
    """تنظيف الكلمة من الرموز + السوابق + اللواحق"""
    w = re.sub(r"[^\u0621-\u064A]", "", raw)
    w = normalize_arabic(w)

    # إزالة السوابق
    for p in sorted(PREFIXES, key=len, reverse=True):
        if w.startswith(p) and len(w) > len(p) + 1:
            w = w[len(p):]
            break

    # إزالة اللواحق
    for s in sorted(SUFFIXES, key=len, reverse=True):
        if w.endswith(s) and len(w) > len(s) + 1:
            w = w[:-len(s)]
            break

    return w

def extract_root_by_pattern(word: str) -> str | None:
    """استخراج الجذر بناءً على الأوزان + القاموس السيادي"""

    w = normalize_token(word)
    n = len(w)
    if n == 0:
        return None

    # 1) القاموس السيادي أولاً
    if w in SOVEREIGN_LEXICON:
        return SOVEREIGN_LEXICON[w]

    # 2) أوزان ثلاثية مزيدة شائعة

    # مستفعل / مستفعلين (مستقيم، مستنصر)
    if w.startswith("مست") and n >= 6:
        core = w[3:]
        if len(core) >= 3:
            return core[:3]

    # مفعول (مغضوب، منصور)
    # م + ف + ع + و + ل
    if w.startswith("م") and "و" in w[2:-1] and n >= 5:
        # مثال: مغضوب → م غ ض و ب
        # نأخذ الحرف 1،2، والأخير
        return w[1] + w[2] + w[-1]

    # فاعل (ضال، قائل)
    # ف ا ع ل
    if n >= 4 and w[1] == "ا":
        # مثال: ضال → ض ا ل → ض ل ل (تقريبًا)
        # مثال: قائل → قايل → قول (تقريبًا)
        root = w[0] + w[2] + (w[3] if n > 3 else w[2])
        root = root.replace("ئ", "و")
        return root

    # افتعل (اختلف، اختبر)
    if n >= 5 and w.startswith("ا") and w[2] == "ت":
        # ا + ف + ت + ع + ل
        return w[1] + w[3] + (w[4] if n > 4 else w[3])

    # انفعل / انفعال (انطلق، انقلب)
    if n >= 5 and w.startswith("ان"):
        return w[2] + w[3] + (w[4] if n > 4 else w[3])

    # 3) الفعل المضارع (يكتب، يستهزئون، يخادعون)
    if n >= 4 and w[0] in {"ي", "ت", "ن", "ا"}:
        core = w[1:]
        if len(core) >= 3:
            return core[:3]

    # 4) إذا كانت ثلاثية → نعتبرها جذرًا
    if n == 3:
        return w

    # 5) fallback تقريبي: أول ثلاثة أحرف بعد التنظيف
    if n > 3:
        return w[:3]

    return w

def analyze_text_v7(text: str):
    """محرك الجذور v7 — تحليل نص كامل"""
    tokens = text.split()
    roots = []

    for t in tokens:
        t_norm = normalize_arabic(t)
        if not t_norm or t_norm in STOPWORDS:
            continue

        cleaned = clean_word(t_norm)
        if not cleaned or cleaned in STOPWORDS:
            continue

        root = extract_root_by_pattern(cleaned)
        if not root:
            continue

        # يمكن هنا تمرير الجذر عبر canonize_root إن أردت
        canonical = canonize_root(root)
        if canonical and len(canonical) >= 3:
            roots.append(canonical)
        elif root and len(root) >= 3:
            roots.append(root)

    freq = Counter(roots).most_common()
    return {
        "root_frequency": freq,
        "total_roots": len(roots),
        "status": "Root Engine v7 — pattern-based",
    }
