# ============================
#   Fusion Engine v2
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root
from utils.ayah_matcher import match_ayahs_by_roots
from utils.tafsir_engine import generate_tafsir

def detect_state(roots):
    if any(r in ["رحم", "غفر", "عفو"] for r in roots):
        return "يبحث عن رحمة ومغفرة"
    elif any(r in ["علم", "عرف", "دري"] for r in roots):
        return "يبحث عن علم وبصيرة"
    elif any(r in ["هدي", "رشد", "قوم"] for r in roots):
        return "يبحث عن هداية وطريق"
    else:
        return "يبحث عن إجابة"

def run_full_analysis(query, quran):
    analysis = analyze_text_v7(query)
    roots = [canonize_root(r) for r, _ in analysis["root_frequency"]]
    roots = [r for r in roots if r and len(r) >= 2]
    
    from utils.ayah_matcher import match_ayahs_by_roots
    matches = match_ayahs_by_roots(roots, quran, top_n=15)
    
    state = detect_state(roots)
    
    if "رحمة" in state:
        guidance = "🕊️ لا تيأس من رحمة الله — إنه الغفور الرحيم."
    elif "علم" in state:
        guidance = "📚 استمر في طلب العلم — فتح باب الفهم قريب."
    elif "هداية" in state:
        guidance = "🧭 أنت على الطريق الصحيح — استمر ولا تتردد."
    else:
        guidance = "💡 تأمل الآيات بعمق — ستجد إجابتك."
    
    return {
        "roots": roots,
        "state": state,
        "guidance": guidance,
        "matches": matches,
        "status": "Fusion Engine v2 with Root Engine v7.0"
    }
