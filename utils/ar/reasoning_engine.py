from utils.semantic_engine import get_similar_ayahs, extract_roots_from_matches
from utils.semantic_layers import context_intersection, semantic_concepts
from utils.root_metrics import analyze_root
from utils.data_loader import load_quran

QURAN = load_quran()

# ============================
# 1) تفسير سبب اختيار الآيات
# ============================
def explain_ayah_similarity(text, matches):
    reasons = []

    # الكلمات المشتركة
    ctx = context_intersection(text, matches)
    if ctx:
        reasons.append(
            f"وجود كلمات مشتركة بين النص والآيات مثل: {', '.join([w for w, _ in ctx[:3]])}"
        )

    # الجذور المشتركة
    roots = extract_roots_from_matches(matches)
    if roots:
        top_root = roots[0][0]
        reasons.append(
            f"الجذر الأكثر ارتباطًا بالنص هو **{top_root}** والذي يظهر في عدة آيات قريبة."
        )

    # المفاهيم الدلالية
    concepts = semantic_concepts(matches)
    if concepts:
        reasons.append(
            f"الآيات تشترك في مفاهيم دلالية مثل: {', '.join([c for c, _ in concepts[:3]])}"
        )

    if not reasons:
        return "تم اختيار الآيات بناءً على التشابه الدلالي العام."

    return "؛ ".join(reasons)


# ============================
# 2) تفسير سبب قوة الجذر
# ============================
def explain_root_strength(root):
    metrics = analyze_root(root)

    reasons = []

    if metrics["strength"] > 20:
        reasons.append("الجذر يظهر في عدد كبير من الآيات، مما يعكس قوة حضوره.")
    elif metrics["strength"] > 5:
        reasons.append("الجذر يظهر في عدة مواضع مختلفة، مما يشير إلى أهميته.")

    if metrics["semantic_diversity"] > 3:
        reasons.append("الجذر يمتلك تنوعًا دلاليًا واسعًا في القرآن.")

    if metrics["context_density"] > 0.2:
        reasons.append("الجذر يظهر في سياقات متعددة مما يزيد من كثافة حضوره.")

    if not reasons:
        return "الجذر له حضور متوسط في القرآن."

    return "؛ ".join(reasons)


# ============================
# 3) تفسير العلاقة بين سورتين
# ============================
def explain_surah_relation(s1, s2, report):
    reasons = []

    if report["similarity"] > 0.3:
        reasons.append("السورتان تتشاركان في بنية دلالية متقاربة.")

    if report["shared_roots"]:
        reasons.append(
            f"وجود جذور مشتركة مثل: {', '.join(report['shared_roots'][:5])}"
        )

    if len(report["unique_roots_1"]) < 5 and len(report["unique_roots_2"]) < 5:
        reasons.append("السورتان تمتلكان طيفًا جذريًا متقاربًا.")

    if not reasons:
        return "العلاقة بين السورتين ضعيفة دلاليًا."

    return "؛ ".join(reasons)