# ============================
#   Root Engine v7.0 — المحرك الجذري السيادي
#   يستخدم Lexicon v7 للتحقق من صحة الجذور
# ============================

import re
from collections import Counter
from utils.root_canonizer import canonize_root
from utils.lexicon_v7 import get_root_info, LEXICON_V7

# الكلمات الضعيفة للإزالة
STOPWORDS = {
    "من", "في", "على", "عن", "إلى", "و", "يا", "ما", "هذا", "هذه",
    "ذلك", "تلك", "ثم", "ف", "ب", "ل", "ك", "إن", "أن", "قد", "هل",
    "أ", "إ", "ألا", "أفلا", "أولم", "ألم", "لعل", "ليت", "هو", "هي",
    "هم", "هن", "نحن", "أنت", "أنتم", "أنتن", "الذي", "التي", "الذين"
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

def validate_root(root):
    """التحقق من صحة الجذر باستخدام Lexicon v7"""
    if root in LEXICON_V7:
        return True
    canonical = canonize_root(root)
    return canonical in LEXICON_V7

def analyze_text_v7(text):
    """
    Root Engine v7.0 - تحليل النص مع التحقق من Lexicon v7
    يضمن عدم ظهور جذور غير قرآنية أو مقاطع صوتية
    """
    words = extract_words(text)
    root_counter = Counter()
    
    for word in words:
        if len(word) >= 3:
            potential_root = word[:3]
            canonical = canonize_root(potential_root)
            
            if canonical and len(canonical) >= 2 and validate_root(canonical):
                root_counter[canonical] += 1
    
    sorted_roots = []
    root_weights = {}
    root_categories = {}
    
    for root, count in root_counter.most_common():
        root_info = get_root_info(root)
        sorted_roots.append((root, count))
        root_weights[root] = root_info.get("weight", 0.5)
        root_categories[root] = root_info.get("category", "عام")
    
    return {
        "root_frequency": sorted_roots,
        "root_weights": root_weights,
        "root_categories": root_categories,
        "total_roots": len(sorted_roots),
        "status": "Root Engine v7.0 - Lexicon Verified"
    }

# للتوافق مع الإصدارات القديمة
analyze_text_v6 = analyze_text_v7
analyze_text_v5 = analyze_text_v7
analyze_text_v4 = analyze_text_v7
