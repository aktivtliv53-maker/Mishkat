# ============================
#   Mishkat Fusion Engine v2.0
#   run_full_analysis + Conscious Integration
# ============================

from utils.root_engine import analyze_text_v5
from utils.reasoning_engine import build_reasoning_path_v4
from utils.root_canonizer import canonize_root
from utils.ayah_matcher import match_ayahs_by_roots
from utils.tafsir_engine import generate_tafsir

def detect_state(roots):
    """تحديد حالة المستخدم بناءً على الجذور"""
    if any(r in ["رحم", "غفر", "عفو"] for r in roots):
        return "يبحث عن رحمة ومغفرة"
    elif any(r in ["علم", "عرف", "دري"] for r in roots):
        return "يبحث عن علم وبصيرة"
    elif any(r in ["هدي", "رشد", "قوم"] for r in roots):
        return "يبحث عن هداية وطريق"
    elif any(r in ["صبر", "ثبت", "حلم"] for r in roots):
        return "يمر بامتحان ويحتاج صبراً"
    elif any(r in ["عبد", "دعو", "صلو"] for r in roots):
        return "يبحث عن قرب من الله"
    else:
        return "يبحث عن إجابة"

def build_journey(roots, matches):
    """بناء مسار قرآني من الآيات"""
    journey = []
    stages = ["بداية", "تأمل", "توجيه", "ختام"]
    for i, stage in enumerate(stages):
        if i < len(matches):
            m = matches[i]
            journey.append({
                "stage": stage,
                "surah": m.get("surah_number"),
                "ayah": m.get("ayah_number"),
                "text": m.get("text", "")
            })
    return journey

def run_full_analysis(query, quran):
    """تحليل كامل للسؤال مع دمج جميع المحركات"""
    
    # 1) تحليل الجذور
    analysis = analyze_text_v5(query)
    roots = [canonize_root(r) for r, _ in analysis["root_frequency"]]
    roots = [r for r in roots if r and len(r) >= 3]
    
    # 2) مطابقة الآيات
    matches = match_ayahs_by_roots(roots, quran, top_n=15)
    
    # 3) حالة المستخدم
    state = detect_state(roots)
    
    # 4) التوجيه
    if "رحمة" in state:
        guidance = "🕊️ لا تيأس من رحمة الله — إنه الغفور الرحيم."
    elif "علم" in state:
        guidance = "📚 استمر في طلب العلم — فتح باب الفهم قريب."
    elif "هداية" in state:
        guidance = "🧭 أنت على الطريق الصحيح — استمر ولا تتردد."
    elif "صبر" in state:
        guidance = "🌱 الصبر مفتاح الفرج — ما تمر به مؤقت."
    else:
        guidance = "💡 تأمل الآيات بعمق — ستجد إجابتك."
    
    # 5) المسار القرآني
    journey = build_journey(roots, matches)
    
    # 6) التفسير
    tafsir_results = []
    for m in matches[:5]:
        tafsir = generate_tafsir(m["text"], state, analysis["root_frequency"])
        tafsir_results.append({
            "ayah": m["text"],
            "tafsir": tafsir
        })
    
    # 7) الاستدلال
    try:
        reasoning = build_reasoning_path_v4(quran, query)
    except Exception as e:
        reasoning = f"تم تحليل السؤال: {query}\nالجذور المستخرجة: {', '.join(roots[:5])}"
    
    return {
        "roots": roots,
        "state": state,
        "guidance": guidance,
        "journey": journey,
        "matches": matches,
        "tafsir": tafsir_results,
        "reasoning": reasoning
    }