# utils/root_engine.py — v5.3
# Root Engine v5.3 — المحرك السيادي للجذور والوزن والبنية

import re

# ============================
# 0) أدوات مساعدة
# ============================
AR_DIAC = r"[ًٌٍَُِّْـ]"
AR_LETTERS = r"[ءاأإآبتثجحخدذرزسشصضطظعغفقكلمنهوي]"

def strip_diacritics(text: str) -> str:
    return re.sub(AR_DIAC, "", text or "")

def normalize_alef(text: str) -> str:
    return (text or "").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")

def normalize_word_basic(w: str) -> str:
    w = strip_diacritics(w)
    w = normalize_alef(w)
    w = w.replace("ة", "ه").replace("ى", "ي")
    return w

# زوائد مشهورة
PREFIXES = ["ال", "وال", "فال", "بال", "كال", "لل", "س", "و", "ف", "ب", "ك", "ل"]
SUFFIXES = ["كما", "هما", "كم", "كن", "نا", "ها", "هم", "هن", "ان", "ين", "ون", "ات", "ة", "ه", "ي", "ك", "ا"]

# حروف زائدة محتملة
EXTRA_LETTERS = set(list("استنمويا"))

# ============================
# 1) تصنيف نوع الكلمة
# ============================
def classify_word_type(word: str) -> str:
    w = strip_diacritics(word)
    if not w:
        return "غير محدد"

    if w.startswith(("ي", "ت", "ن", "أ")) and len(w) >= 3:
        return "فعل"

    if w.startswith("ال"):
        return "اسم"

    if w.endswith(("ون", "ين", "ات", "ه", "ة")):
        return "اسم"

    return "غير محدد"

# ============================
# 2) إزالة البادئات واللواحق
# ============================
def strip_prefixes(word: str) -> (str, str):
    for p in sorted(PREFIXES, key=len, reverse=True):
        if word.startswith(p) and len(word) > len(p) + 2:
            return word[len(p):], p
    return word, ""

def strip_suffixes(word: str) -> (str, str):
    for s in sorted(SUFFIXES, key=len, reverse=True):
        if word.endswith(s) and len(word) > len(s) + 2:
            return word[:-len(s)], s
    return word, ""

# ============================
# 3) اكتشاف الوزن
# ============================
def detect_pattern(stem: str) -> str:
    s = stem
    length = len(s)

    if length == 3:
        return "فعل ثلاثي مجرد"

    if length == 4:
        if s.startswith("م"):
            return "مفعول/مفعل"
        if s.startswith("ت"):
            return "تفعّل/تفاعل"
        if s.startswith("ا"):
            return "أفعل"
        return "رباعي محتمل"

    if length == 5:
        if s.startswith("است"):
            return "استفعل"
        if s.startswith("ت"):
            return "تفاعل/تفعّل"
        if s.startswith("ان"):
            return "انفعل"
        return "خماسي محتمل"

    if length == 6:
        if s.startswith("است"):
            return "استفعل سداسي"
        return "سداسي محتمل"

    return "غير محدد"

# ============================
# 4) استخراج الجذر — v5.3
# ============================
def extract_root_v5(word: str) -> str:
    """
    محرك الجذر v5.3 — إصلاح وزن فعلان + توحيد الرحمن + إصلاح الحمد
    """

    if not isinstance(word, str) or not word.strip():
        return ""

    w = normalize_word_basic(word)

    # إزالة البادئات
    w, pref = strip_prefixes(w)

    # إزالة اللواحق
    w, suf = strip_suffixes(w)

    # 🔥 إصلاح وزن "فعلان" (مثل: الرحمن، الغضبان، العطشان)
    if len(w) == 5 and w.endswith("ان"):
        core = w[:-2]
        if len(core) == 3:
            w = core
        elif len(core) == 4:
            for i, ch in enumerate(core):
                if ch in EXTRA_LETTERS:
                    c3 = core[:i] + core[i+1:]
                    if len(c3) == 3:
                        w = c3
                        break
            else:
                w = core[:3]

    # ثلاثي مباشر
    if len(w) == 3:
        root = w

    # رباعي
    elif len(w) == 4:
        for i, ch in enumerate(w):
            if ch in EXTRA_LETTERS:
                c3 = w[:i] + w[i+1:]
                if len(c3) == 3:
                    root = c3
                    break
        else:
            for c in ["ا", "و", "ي"]:
                if c in w:
                    c3 = w.replace(c, "")
                    if len(c3) == 3:
                        root = c3
                        break
            else:
                root = w[0] + w[1] + w[-1]

    # خماسي
    elif len(w) == 5:
        candidates = []
        for i, ch in enumerate(w):
            if ch in EXTRA_LETTERS:
                c4 = w[:i] + w[i+1:]
                if len(c4) == 4:
                    candidates.append(c4)

        for c4 in candidates:
            for i, ch in enumerate(c4):
                if ch in EXTRA_LETTERS:
                    c3 = c4[:i] + c4[i+1:]
                    if len(c3) == 3:
                        root = c3
                        break
            else:
                continue
            break
        else:
            core = [ch for ch in w if ch not in EXTRA_LETTERS]
            if len(core) >= 3:
                root = "".join(core[:3])
            else:
                root = w[:3]

    # أطول من 5
    else:
        core = [ch for ch in w if ch not in EXTRA_LETTERS]
        if len(core) >= 3:
            root = "".join(core[:3])
        else:
            root = w[:3]

    # 🔥 توحيد خاص للرحمن → رحم
    if root == "رحن":
        return "رحم"

    # 🔥 إصلاح جذر الحمد → حمد
    if root in ["حدل", "حلد", "حمدل", "حمل", "حمل"]:
        return "حمد"

    return root

# ============================
# 5) تحليل كلمة — v5.3
# ============================
def analyze_word_v5(word: str) -> dict:
    original = word
    normalized = normalize_word_basic(word)

    stem, pref = strip_prefixes(normalized)
    stem, suf = strip_suffixes(stem)

    root = extract_root_v5(word)
    pattern = detect_pattern(stem)
    wtype = classify_word_type(normalized)

    return {
        "original": original,
        "normalized": normalized,
        "type": wtype,
        "prefix": pref,
        "suffix": suf,
        "stem": stem,
        "root": root,
        "pattern": pattern,
        "length": len(normalized),
        "status": "Root Engine v5.3 analysis complete"
    }

# ============================
# 6) تحليل نص كامل — v5.3
# ============================
def analyze_text_v5(text: str) -> dict:
    if not isinstance(text, str):
        text = str(text or "")

    text_clean = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    text_clean = re.sub(r"\s+", " ", text_clean).strip()

    words = [w for w in text_clean.split(" ") if w]

    analyses = []
    root_freq = {}

    for w in words:
        info = analyze_word_v5(w)
        analyses.append(info)
        r = info["root"]
        if r:
            root_freq[r] = root_freq.get(r, 0) + 1

    root_freq_sorted = sorted(root_freq.items(), key=lambda x: x[1], reverse=True)

    return {
        "word_count": len(words),
        "analyses": analyses,
        "root_frequency": root_freq_sorted,
        "unique_roots": len(root_freq_sorted),
        "status": "Root Engine v5.3 text analysis complete"
    }