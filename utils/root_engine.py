# ============================
#   Root Engine v6.6
#   Enhanced Root Extraction + Canonicalization
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

def analyze_text_v5(text):
    """Root Engine v5 - تحليل أساسي للتوافق مع الإصدارات القديمة"""
    words = extract_words(text)
    root_counter = Counter()
    
    for word in words:
        if len(word) >= 3:
            root = word[:3]
            root_counter[root] += 1
    
    word_analysis = []
    for w in words[:20]:
        word_analysis.append({
            "word": w,
            "letters": list(w),
            "length": len(w)
        })
    
    return {
        "root_frequency": list(root_counter.most_common()),
        "word_analysis": word_analysis,
        "status": "Root Engine v5"
    }

def analyze_text_v6(text):
    """
    Root Engine v6.6 - تحليل النص مع canonicalization محسن
    """
    words = extract_words(text)
    root_counter = Counter()
    
    for word in words:
        if len(word) >= 3:
            # محاولة استخراج جذر ثلاثي
            potential_root = word[:3]
            canonical = canonize_root(potential_root)
            if canonical and len(canonical) >= 2:
                root_counter[canonical] += 1
    
    word_analysis = []
    for w in words[:20]:
        word_analysis.append({
            "word": w,
            "letters": list(w),
            "length": len(w)
        })
    
    return {
        "root_frequency": list(root_counter.most_common()),
        "word_analysis": word_analysis,
        "status": "Root Engine v6.6"
    }

# للتوافق مع الإصدارات القديمة
analyze_text_v4 = analyze_text_v5
