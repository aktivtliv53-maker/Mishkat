import re

def extract_mishkat_root(text):
    """
    استخلاص الجذر وتحليله وفق منطق مشكاة (تطهير السوابق واللواحق)
    """
    # تنظيف النص من علامات التشكيل والرموز
    text = re.sub(r'[^\w\s]', '', text)
    
    # قائمة السوابق واللواحق الشائعة
    prefixes = ['ال', 'ب', 'و', 'ف', 'س']
    for p in prefixes:
        if text.startswith(p) and len(text) > 3:
            text = text[len(p):]
            
    # تحديد الطور الدلالي بناءً على بنية الحروف (هندسة الحروف)
    phase = "light" 
    if any(char in text for char in ['ق', 'د', 'ر']): phase = "power"
    if any(char in text for char in ['ز', 'ك', 'ي']): phase = "purification"
    if any(char in text for char in ['ر', 'ح', 'م']): phase = "mercy"
    
    return {"root": text, "phase": phase}

def calculate_q_index(root):
    """حساب مؤشر الوعي (Q-Index) بناءً على القيم الرقمية للحروف أو تكرارها"""
    # حالياً يعيد قيمة افتراضية سيتم ربطها لاحقاً بمعادلة هندسة الحروف
    return len(root) * 0.33
