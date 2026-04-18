# ============================================
#   Mishkat Comparative Engine v12
#   (Root–Semantic–Existential Comparison)
# ============================================

from utils.root_engine import analyze_text_v6
from utils.root_canonizer import canonize_root


# -------------------------------------------
# 1) استخراج الجذور المعيارية للنص
# -------------------------------------------

def extract_canonical_roots(text: str):
    analysis = analyze_text_v6(text)
    roots = [canonize_root(r) for r, _ in analysis["root_frequency"]]
    return roots


# -------------------------------------------
# 2) حساب العلاقة الدلالية بين الجذور
# -------------------------------------------

SEMANTIC_FIELDS = {
    "عبد": "العبودية والتوجّه",
    "ملك": "السيادة والسلطة",
    "دين": "الجزاء والحساب",
    "يوم": "الزمان والحدث"
}

def semantic_field(root):
    return SEMANTIC_FIELDS.get(root, "غير محدد")


# -------------------------------------------
# 3) حساب العلاقة الوجودية بين الجذور
# -------------------------------------------

EXISTENTIAL_RELATIONS = {
    ("عبد", "ملك"): ("تكامل وجودي", 0.92),
    ("ملك", "دين"): ("ترابط سببي", 0.85),
    ("عبد", "دين"): ("ترابط عبادي–جزائي", 0.88),
}

def existential_relation(r1, r2):
    if (r1, r2) in EXISTENTIAL_RELATIONS:
        return EXISTENTIAL_RELATIONS[(r1, r2)]
    if (r2, r1) in EXISTENTIAL_RELATIONS:
        return EXISTENTIAL_RELATIONS[(r2, r1)]
    return ("لا توجد علاقة وجودية مباشرة", 0.0)


# -------------------------------------------
# 4) حساب المسافة الجذرية
# -------------------------------------------

def root_distance(r1, r2):
    if r1 == r2:
        return 0.0
    if (r1, r2) in EXISTENTIAL_RELATIONS or (r2, r1) in EXISTENTIAL_RELATIONS:
        return 0.4
    return 1.0


# -------------------------------------------
# 5) بناء التقرير النهائي
# -------------------------------------------

def compare_texts_v12(t1: str, t2: str):
    roots1 = extract_canonical_roots(t1)
    roots2 = extract_canonical_roots(t2)

    set1 = set(roots1)
    set2 = set(roots2)

    shared = list(set1 & set2)
    unique_1 = list(set1 - set2)
    unique_2 = list(set2 - set1)

    # العلاقات الوجودية
    existential_links = []
    for r1 in set1:
        for r2 in set2:
            rel, strength = existential_relation(r1, r2)
            if strength > 0:
                existential_links.append({
                    "root_1": r1,
                    "root_2": r2,
                    "relation": rel,
                    "strength": strength
                })

    # المسافة الجذرية
    distances = []
    for r1 in set1:
        for r2 in set2:
            distances.append({
                "root_1": r1,
                "root_2": r2,
                "distance": root_distance(r1, r2)
            })

    return {
        "shared_roots": shared,
        "unique_1": unique_1,
        "unique_2": unique_2,

        "semantic_fields": {
            r: semantic_field(r) for r in (set1 | set2)
        },

        "existential_relations": existential_links,
        "root_distances": distances,

        "status": "Comparative Engine v12 — Deep Semantic Mode"
    }
