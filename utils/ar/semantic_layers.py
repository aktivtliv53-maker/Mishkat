# utils/semantic_layers.py

def context_intersection(roots1, roots2):
    """إيجاد الجذور المشتركة بين مجموعتين."""
    try:
        return list(set(roots1) & set(roots2))
    except:
        return []

def semantic_concepts(roots):
    """تحويل الجذور إلى مفاهيم بسيطة (Placeholder)."""
    concepts = []
    for r in roots:
        concepts.append(f"مفهوم مرتبط بالجذر: {r}")
    return concepts