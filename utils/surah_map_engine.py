# ============================
#   Surah Map Engine v7 — Root Network Edition
#   (نسخة كاملة — جاهزة — مستقرة)
# ============================

from utils.root_engine_v7 import analyze_text_v7

# ------------------------------------
# 1) استخراج جذور السورة
# ------------------------------------
def extract_surah_roots(quran, surah_number):
    ayahs = [a for a in quran if a["surah_number"] == surah_number]
    all_roots = []

    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        roots = [r for r, c in analysis["root_frequency"]]
        all_roots.extend(roots)

    return all_roots


# ------------------------------------
# 2) بناء شبكة الجذور داخل السورة
# ------------------------------------
def build_surah_map(quran, surah_number):
    ayahs = [a for a in quran if a["surah_number"] == surah_number]

    nodes = {}
    links = {}

    for ayah in ayahs:
        analysis = analyze_text_v7(ayah["text"])
        roots = [r for r, c in analysis["root_frequency"]]

        # إضافة الجذور كعُقد
        for r in roots:
            if r not in nodes:
                nodes[r] = {"id": r, "count": 0}
            nodes[r]["count"] += 1

        # بناء الروابط (co-occurrence)
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                pair = tuple(sorted([roots[i], roots[j]]))
                if pair not in links:
                    links[pair] = 0
                links[pair] += 1

    # تحويل الروابط إلى قائمة
    link_list = []
    for (a, b), w in links.items():
        link_list.append({
            "source": a,
            "target": b,
            "weight": w
        })

    # تحويل العقد إلى قائمة
    node_list = []
    for r, data in nodes.items():
        node_list.append({
            "id": r,
            "weight": data["count"]
        })

    return {
        "surah": surah_number,
        "nodes": node_list,
        "links": link_list,
        "status": "Surah Map v7 — Root Network Active"
    }


# ------------------------------------
# 3) إحصاءات السورة
# ------------------------------------
def get_surah_stats(quran, surah_number):
    data = build_surah_map(quran, surah_number)
    return {
        "unique_roots": len(data["nodes"]),
        "connections": len(data["links"]),
        "max_weight": max([n["weight"] for n in data["nodes"]]) if data["nodes"] else 0
    }
