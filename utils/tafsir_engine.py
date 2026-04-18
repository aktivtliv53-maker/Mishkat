# ============================
#   Mishkat Tafsir Engine v1.0
#   (Root-Based Interpretation)
# ============================

def generate_tafsir(ayah_text, direction, root_freq):
    """توليد تفسير ذكي للآية بناءً على الجذور والاتجاه"""
    roots = [r for r, _ in root_freq]

    tafsir = f"🔹 تفسير موجّه ({direction}):\n"
    tafsir += f"الآية تشير إلى معنى مرتبط بجذور: {', '.join(roots[:5])}.\n"

    if "رحم" in direction or "رحمة" in direction:
        tafsir += "الآية تحمل إشارات للطمأنينة واللطف الإلهي."
    elif "قوة" in direction:
        tafsir += "الآية تدعو إلى الثبات واتخاذ القرار."
    elif "علم" in direction:
        tafsir += "الآية تفتح باب الفهم والبصيرة."
    elif "حركة" in direction:
        tafsir += "الآية تحث على المبادرة وعدم التوقف."
    elif "خلق" in direction:
        tafsir += "الآية تشير إلى بداية جديدة أو تحول."
    elif "هداية" in direction:
        tafsir += "الآية ترشدك إلى الطريق المستقيم."
    elif "صبر" in direction:
        tafsir += "الآية تعلمك أن الصبر مفتاح الفرج."
    else:
        tafsir += "الآية تحمل توازنًا بين المعاني، تأملها بعمق."

    return tafsir

def get_tafsir_for_ayah(ayah_text):
    """تفسير سريع للآية بدون تحليل جذور"""
    if not ayah_text:
        return "لا يوجد تفسير متاح"
    
    if any(w in ayah_text for w in ["رحمة", "رحيم", "غفور"]):
        return "🔹 الآية تشير إلى رحمة الله الواسعة التي وسعت كل شيء."
    elif any(w in ayah_text for w in ["صبر", "اصبر", "احتسب"]):
        return "🔹 الآية تحث على الصبر والاحتساب، فالعاقبة للمتقين."
    elif any(w in ayah_text for w in ["علم", "يعلم", "تفكر"]):
        return "🔹 الآية تدعو إلى التفكر والعلم، فالله عليم بكل شيء."
    elif any(w in ayah_text for w in ["اتقوا", "افعلوا", "لا تفعلوا"]):
        return "🔹 الآية تحتوي على توجيه إلهي مباشر للعباد."
    elif any(w in ayah_text for w in ["خلق", "بدأ", "أنشأ"]):
        return "🔹 الآية تتحدث عن قدرة الله على الخلق والإبداع."
    else:
        return "🔹 تأمل هذه الآية، فهي تحمل في طياتها إجابة لسؤالك."