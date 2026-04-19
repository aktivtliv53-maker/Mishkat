# ============================
#   Gene Spectrum Engine v5
#   متوافق مع Root Engine v7.0 (بدون root_canonizer)
# ============================

from utils.root_engine_v7 import analyze_text_v7

def compute_gene_spectrum_v5(text):
    """حساب الطيف الجيني للنص"""
    analysis = analyze_text_v7(text)
    roots = analysis["root_frequency"]
    
    # تجميع الجذور حسب أول حرف (تصنيف بسيط)
    categories = {}
    for root, count in roots:
        first_letter = root[0] if root else "?"
        if first_letter not in categories:
            categories[first_letter] = 0
        categories[first_letter] += count
    
    return {
        "roots": roots,
        "categories": categories,
        "total_roots": len(roots),
        "status": "Gene Spectrum v5 with Root Engine v7.0"
    }
