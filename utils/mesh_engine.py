# ============================
#   Mesh Networks v3 — Final
#   Fully Compatible with Root Engine v7
#   No canonize_root, No legacy imports
# ============================

from utils.root_engine_v7 import analyze_text_v7
from collections import Counter

def build_mesh_networks_v3(quran, surah_number):
    """
    بناء شبكة الجذور لسورة واحدة باستخدام Root Engine v7
    - nodes: الجذور + وزن كل جذر
    - links: العلاقات بين الجذور داخل كل آية
    """

    # 1) جمع آيات السورة
    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    # 2) استخراج جميع الجذور
    all_roots = []
    per_ayah_roots = []

    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        roots = [root for root, _ in analysis["root_frequency"]]
        per_ayah_roots.append(roots)
        all_roots.extend(roots)

    # 3) حساب تكرار الجذور
    root_counts = Counter(all_roots)

    nodes = [
        {"id": root, "weight": count}
        for root, count in root_counts.items()
    ]

    # 4) بناء الروابط (co-occurrence)
    edges = {}

    for roots in per_ayah_roots:
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                pair = tuple(sorted([roots[i], roots[j]]))
                edges[pair] = edges.get(pair, 0) + 1

    links = [
        {"source": a, "target": b, "weight": w}
        for (a, b), w in edges.items()
    ]

    return {
        "nodes": nodes,
        "links": links,
        "root_count": len(nodes),
        "link_count": len(links),
        "status": "Mesh Networks v3 — Root Engine v7"
    }
