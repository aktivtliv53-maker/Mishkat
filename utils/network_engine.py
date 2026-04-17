# utils/network_engine.py — v11
# محرك الشبكات السيادية — Mesh Networks v2
# يشمل:
# - شبكة الآيات
# - شبكة الجذور
# - شبكة السور
# - الشبكات الشبكية (Mesh Networks v2)

from utils.semantic_engine import extract_roots_from_text

# ============================================================
# 1) شبكة الآيات — Ayah Network
# ============================================================
def build_ayah_network(quran):
    """
    شبكة تربط كل آية بالآيات التي تشترك معها في الجذور.
    """
    network = {}

    # استخراج جذور كل آية
    ayah_roots = []
    for ay in quran:
        roots = extract_roots_from_text(ay["text"])
        ayah_roots.append(roots)

    # بناء الشبكة
    for i, roots_i in enumerate(ayah_roots):
        links = []
        for j, roots_j in enumerate(ayah_roots):
            if i == j:
                continue
            shared = set(roots_i) & set(roots_j)
            if len(shared) > 0:
                links.append({
                    "ayah_index": j,
                    "shared_roots": list(shared),
                    "weight": len(shared)
                })

        network[i] = {
            "ayah": quran[i],
            "links": links
        }

    return network

# ============================================================
# 2) شبكة الجذور — Root Graph
# ============================================================
def build_root_graph(quran):
    """
    شبكة تربط كل جذر بالآيات التي يظهر فيها.
    """
    graph = {}

    for idx, ay in enumerate(quran):
        roots = extract_roots_from_text(ay["text"])
        for r in roots:
            if r not in graph:
                graph[r] = []
            graph[r].append({
                "ayah_index": idx,
                "surah": ay["surah_number"],
                "ayah": ay["ayah_number"]
            })

    return graph

# ============================================================
# 3) شبكة السور — Surah Network
# ============================================================
def build_surah_network(quran):
    """
    شبكة تربط السور ببعضها بناءً على الجذور المشتركة.
    """
    # جمع جذور كل سورة
    surah_roots = {}
    for ay in quran:
        s = ay["surah_number"]
        if s not in surah_roots:
            surah_roots[s] = []
        surah_roots[s].extend(extract_roots_from_text(ay["text"]))

    # بناء الشبكة
    network = {}
    surahs = sorted(surah_roots.keys())

    for s1 in surahs:
        links = []
        for s2 in surahs:
            if s1 == s2:
                continue
            shared = set(surah_roots[s1]) & set(surah_roots[s2])
            if len(shared) > 0:
                links.append({
                    "surah": s2,
                    "shared_roots": list(shared),
                    "weight": len(shared)
                })

        network[s1] = {
            "surah": s1,
            "links": links
        }

    return network

# ============================================================
# 4) Mesh Networks v2 — Ayah / Root / Surah Mesh
# ============================================================
def build_mesh_networks(quran):
    """
    يبني 3 شبكات مترابطة:
    - شبكة الآيات
    - شبكة الجذور
    - شبكة السور
    ويجمعها في بنية واحدة.
    """

    ayah_net = build_ayah_network(quran)
    root_net = build_root_graph(quran)
    surah_net = build_surah_network(quran)

    mesh = {
        "ayah_mesh": ayah_net,
        "root_mesh": root_net,
        "surah_mesh": surah_net,
        "status": "Mesh Networks v2 built successfully"
    }

    return mesh