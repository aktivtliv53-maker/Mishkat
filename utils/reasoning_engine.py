# ============================
#   Reasoning Engine v4
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root

def build_reasoning_path_v4(quran, query):
    """بناء مسار الاستدلال"""
    analysis = analyze_text_v7(query)
    roots = [r for r, _ in analysis["root_frequency"]]
    
    return {
        "query": query,
        "roots": roots,
        "categories": [analysis["root_categories"].get(r, "عام") for r in roots],
        "status": "Reasoning Engine v4 with Root Engine v7.0"
    }
