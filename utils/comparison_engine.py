# ============================
#   Comparison Engine v12
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root

def compare_texts_v12(text1, text2):
    """مقارنة نصين واستخراج الجذور المشتركة والفريدة"""
    
    # تحليل النصين باستخدام Root Engine v7.0
    analysis1 = analyze_text_v7(text1)
    analysis2 = analyze_text_v7(text2)
    
    roots1 = {r: c for r, c in analysis1["root_frequency"]}
    roots2 = {r: c for r, c in analysis2["root_frequency"]}
    
    # الجذور المشتركة
    shared = set(roots1.keys()) & set(roots2.keys())
    
    # الجذور الفريدة لكل نص
    unique_1 = set(roots1.keys()) - set(roots2.keys())
    unique_2 = set(roots2.keys()) - set(roots1.keys())
    
    # حساب درجات التشابه
    if not roots1 or not roots2:
        similarity = 0
    else:
        common_score = sum(min(roots1.get(r, 0), roots2.get(r, 0)) for r in shared)
        total_score = sum(roots1.values()) + sum(roots2.values())
        similarity = (2 * common_score / total_score) if total_score > 0 else 0
    
    return {
        "shared_roots": list(shared),
        "unique_roots_1": list(unique_1),
        "unique_roots_2": list(unique_2),
        "roots_1": roots1,
        "roots_2": roots2,
        "similarity": similarity,
        "status": "Comparison Engine v12 with Root Engine v7.0"
    }

# للتوافق مع الإصدارات القديمة
compare_texts_v4 = compare_texts_v12
