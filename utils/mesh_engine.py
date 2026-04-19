# ============================
#   Mesh Networks v3
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root

def build_mesh_networks_v3(quran, surah_number):
    """بناء شبكة الجذور للسورة"""
    ayahs = [a for a in quran if a["surah_number"] == surah_number]
    
    all_roots = []
    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        for root, _ in analysis["root_frequency"]:
            canonical = canonize_root(root)
            if canonical:
                all_roots.append(canonical)
    
    # حساب التكرارات
    from collections import Counter
    root_counts = Counter(all_roots)
    
    nodes = [{"id": r, "weight": c} for r, c in root_counts.items()]
    
    # بناء الروابط (بسيط: الجذور التي تظهر في نفس الآية)
    edges = {}
    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        ayah_roots = [canonize_root(r) for r, _ in analysis["root_frequency"] if canonize_root(r)]
        for i in range(len(ayah_roots)):
            for j in range(i+1, len(ayah_roots)):
                pair = tuple(sorted([ayah_roots[i], ayah_roots[j]]))
                edges[pair] = edges.get(pair, 0) + 1
    
    links = [{"source": a, "target": b, "weight": w} for (a, b), w in edges.items()]
    
    return {
        "nodes": nodes,
        "links": links,
        "root_count": len(nodes),
        "link_count": len(links),
        "status": "Mesh Networks v3 with Root Engine v7.0"
    }
