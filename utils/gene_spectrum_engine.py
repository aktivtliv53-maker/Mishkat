# ============================
#   Gene Spectrum Engine v6
#   Uses Root Engine v6.6
# ============================

from utils.root_engine import analyze_text_v6
from utils.root_canonizer import canonize_root

def compute_gene_spectrum_v5(text: str):
    """تحليل الطيف الجيني باستخدام Root Engine v6.6"""
    analysis = analyze_text_v6(text)

    freq = {}
    for root, count in analysis["root_frequency"]:
        canon = canonize_root(root)
        if canon and len(canon) >= 2:
            freq[canon] = freq.get(canon, 0) + count

    freq_sorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return {
        "unique_roots": len(freq_sorted),
        "root_frequency": freq_sorted,
        "top_roots": freq_sorted[:50],
        "status": "Gene Spectrum v6 computed (Root Engine v6.6)"
    }
