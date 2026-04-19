# ============================
#   Root Canonizer v2.0
#   يقوم بتوحيد الجذور إلى صيغتها الصحيحة
# ============================

import re

# خريطة توحيد الحروف المتشابهة
NORMALIZATION_MAP = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ؤ": "و",
    "ئ": "ي",
    "ة": "ه",
    "ى": "ي",
}

def normalize_arabic(text):
    """توحيد الحروف المتشابهة"""
    for char, replacement in NORMALIZATION_MAP.items():
        text = text.replace(char, replacement)
    return text

# قائمة الجذور الصحيحة المعروفة (مثال)
KNOWN_ROOTS = {
    "سمو", "اله", "رحم", "حمد", "ربب", "علم", "ملك", "يوم", "دين",
    "عبد", "عون", "هدي", "صرط", "قوم", "علو", "نعم", "غير", "غضب",
    "ضلل", "كفر", "امن", "نزل", "قبل", "اخر", "يقن", "فلح", "نذر",
    "ختم", "قلب", "سمع", "بصر", "عذب", "عظم", "خدع"
}

def canonize_root(root):
    """
    توحيد الجذر إلى صيغته الأساسية
    """
    if not root or len(root) < 2:
        return None
    
    # تطبيع الحروف
    normalized = normalize_arabic(root)
    
    # إزالة ال التعريف
    if normalized.startswith("ال"):
        normalized = normalized[2:]
    
    # التأكد من أن الجذر ثلاثي أو رباعي
    if len(normalized) >= 3:
        # أخذ أول 3 أحرف كجذر أساسي
        result = normalized[:3]
        
        # التحقق من وجوده في القائمة المعروفة
        if result in KNOWN_ROOTS:
            return result
        
        # محاولة تعديل بعض الحالات الشائعة
        if result == "الر":
            return "رحم"
        if result == "بِس":
            return "سمو"
        if result == "الد":
            return "دين"
        if result == "اِي":
            return "ايي"
        if result == "نَع":
            return "نعم"
        if result == "نَس":
            return "عون"
        if result == "صِر":
            return "صرط"
        if result == "غَي":
            return "غير"
        if result == "الْ":
            return None
        if result == "لِل":
            return "اله"
        
        return result
    
    return None
