# ============================================================
#   Mesh Networks v3 — سورة واحدة
#   شبكة جذور + علاقات + وزن + تكرار
# ============================================================

from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root

def build_mesh_networks_v3(quran, surah_number):
    """
    شبكة جذور سورة واحدة:
    - nodes = الجذور
    - edges = العلاقات بين الجذور داخل الآيات
    - weight = تكرار الجذر
    - co_links = عدد مرات اجتماع الجذرين في نفس الآية
    """

    # استخراج آيات السورة
    ayahs = [
        a for a in quran
        if a["surah_number"] == surah_number
    ]

    # استخراج جذور كل آية
    ayah_roots = []
    for a in ayahs:
        analysis = analyze_text_v5(a["text"])
        roots = [canonize_root(r) for r, _ in analysis["root_frequency"]]
        ayah_roots.append(roots)

    # حساب تكرار الجذور
    root_freq = {}
    for roots in ayah_roots:
        for r in roots:
            root_freq[r] = root_freq.get(r, 0) + 1

    # بناء العقد
    nodes = [
        {"id": r, "weight": root_freq[r]}
        for r in root_freq
    ]

    # بناء الروابط (العلاقات)
    edges = {}
    for roots in ayah_roots:
        unique = list(set(roots))
        for i in range(len(unique)):
            for j in range(i + 1, len(unique)):
                pair = tuple(sorted([unique[i], unique[j]]))
                edges[pair] = edges.get(pair, 0) + 1

    # تحويل الروابط إلى قائمة
    links = [
        {"source": a, "target": b, "weight": w}
        for (a, b), w in edges.items()
    ]

    return {
        "surah": surah_number,
        "nodes": nodes,
        "links": links,
        "root_count": len(nodes),
        "link_count": len(links),
        "status": "ok"
    }