import re

# ---------------------------------------------------------
# 1) استخراج الجذر وتحديد الطور الدلالي (Mishkat Root Engine)
# ---------------------------------------------------------
def extract_mishkat_root(word):
    """
    استخلاص الجذر وتحليله وفق منطق مشكاة (تطهير السوابق واللواحق)
    """
    if not isinstance(word, str):
        return {"root": "", "phase": "light"}

    # إزالة الرموز
    w = re.sub(r'[^\u0621-\u064A\s]', '', word)

    # السوابق الشائعة
    prefixes = ['ال', 'ب', 'و', 'ف', 'س']
    for p in prefixes:
        if w.startswith(p) and len(w) > 3:
            w = w[len(p):]

    # تحديد الطور الدلالي
    phase = "light"
    if any(c in w for c in ['ق', 'د', 'ر']):
        phase = "power"
    if any(c in w for c in ['ز', 'ك', 'ي']):
        phase = "purification"
    if any(c in w for c in ['ر', 'ح', 'م']):
        phase = "mercy"

    return {"root": w, "phase": phase}


# ---------------------------------------------------------
# 2) حساب مؤشر الوعي (Q-Index)
# ---------------------------------------------------------
def calculate_q_index(root):
    """
    حساب مؤشر الوعي بناءً على طول الجذر (مؤقتًا)
    """
    return len(root) * 0.33


# ---------------------------------------------------------
# 3) بناء شبكة الجذور (Nodes + Edges)
# ---------------------------------------------------------
def build_root_graph(words):
    """
    بناء شبكة جذور من الكلمات المستخرجة
    """
    nodes = []
    edges = []

    last_root = None

    for w in words:
        info = extract_mishkat_root(w)
        root = info["root"]
        phase = info["phase"]

        # عقدة
        nodes.append({
            "id": root,
            "label": root,
            "semantic_phase": phase
        })

        # رابط بين الجذور المتتابعة
        if last_root and last_root != root:
            edges.append({
                "source": last_root,
                "target": root,
                "weight": 1
            })

        last_root = root

    return nodes, edges


# ---------------------------------------------------------
# 4) المعالج الرئيسي — Mishkat Processor
# ---------------------------------------------------------
def process_text(text):
    """
    المعالج الموحد الذي ينتج:
    - جذور
    - أطوار دلالية
    - Q-index
    - شبكة جذور كاملة
    """
    if not isinstance(text, str):
        return {}

    # تقسيم النص
    words = text.split()

    # استخراج الجذور
    roots_info = [extract_mishkat_root(w) for w in words]
    roots = [r["root"] for r in roots_info]

    # حساب Q-index
    q_index = sum(calculate_q_index(r) for r in roots)

    # بناء الشبكة
    graph_nodes, graph_edges = build_root_graph(words)

    # الحالة النهائية
    return {
        "raw_text": text,
        "words": words,
        "roots": roots,
        "semantic_phases": [r["phase"] for r in roots_info],
        "q_index": q_index,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges
    }
