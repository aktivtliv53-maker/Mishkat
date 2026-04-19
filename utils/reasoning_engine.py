# ============================
#   Reasoning Engine v4
#   متوافق مع Root Engine v7.0 (بدون root_canonizer)
# ============================

from utils.root_engine_v7 import analyze_text_v7

def build_reasoning_path_v4(quran, query):
    """بناء مسار الاستدلال"""
    analysis = analyze_text_v7(query)
    roots = [r for r, _ in analysis["root_frequency"]]
    
    # تصنيف بسيط حسب أول حرف
    categories = {}
    for root in roots:
        first = root[0] if root else "?"
        if first not in categories:
            categories[first] = []
        categories[first].append(root)
    
    return {
        "query": query,
        "roots": roots,
        "categories": categories,
        "total_roots": len(roots),
        "status": "Reasoning Engine v4 with Root Engine v7.0"
    }
