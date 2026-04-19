# ============================
#   Gene Spectrum Engine v5
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root
from utils.lexicon_v7 import get_root_category

def compute_gene_spectrum_v5(text):
    """حساب الطيف الجيني للنص"""
    analysis = analyze_text_v7(text)
    roots = analysis["root_frequency"]
    
    # تجميع الجذور حسب الفئة باستخدام lexicon_v7
    categories = {}
    for root, count in roots:
        category = get_root_category(root)
        if category not in categories:
            categories[category] = 0
        categories[category] += count
    
    return {
        "roots": roots,
        "categories": categories,
        "total_roots": len(roots),
        "status": "Gene Spectrum v5 with Root Engine v7.0"
    }
