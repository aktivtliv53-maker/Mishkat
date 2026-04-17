# ============================
#   Conscious Map Engine v1.0
#   build_conscious_map
# ============================

from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root
from utils.tafsir_engine import generate_tafsir

def get_key_ayahs(quran, surah_num, top_n=5):
    """استخراج الآيات المحورية من السورة"""
    ayahs = [a for a in quran if a.get("surah_number") == surah_num]
    
    # تحليل كل آية وحساب وزنها
    scored = []
    for ay in ayahs:
        analysis = analyze_text_v5(ay["text"])
        score = sum(c for _, c in analysis["root_frequency"])
        scored.append((ay, score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]

def build_reasoning_fallback(text, max_length=500):
    """نسخة مبسطة من الاستدلال في حال تعذر استخدام المحرك الأصلي"""
    if not text:
        return "لا يوجد نص للتحليل"
    
    # تحليل بسيط
    analysis = analyze_text_v5(text[:max_length])
    roots = [r for r, _ in analysis["root_frequency"][:5]]
    
    return {
        "text": text[:200] + "...",
        "roots": roots,
        "message": f"تم تحليل النص واستخراج الجذور: {', '.join(roots) if roots else 'لا توجد جذور واضحة'}"
    }

def build_conscious_map(surah_num, quran):
    """بناء خريطة واعية للسورة"""
    
    # 1) استخراج الجذور
    ayahs = [a for a in quran if a.get("surah_number") == surah_num]
    all_roots = []
    for ay in ayahs:
        analysis = analyze_text_v5(ay["text"])
        for r, _ in analysis["root_frequency"]:
            cr = canonize_root(r)
            if cr and len(cr) >= 3:
                all_roots.append(cr)
    
    # إزالة التكرار مع الحفاظ على الترتيب
    unique_roots = []
    for r in all_roots:
        if r not in unique_roots:
            unique_roots.append(r)
    
    # 2) الآيات المحورية
    key_ayahs = get_key_ayahs(quran, surah_num)
    
    # 3) التفسير
    tafsir_results = []
    for ay in key_ayahs[:5]:
        analysis = analyze_text_v5(ay["text"])
        tafsir = generate_tafsir(ay["text"], "تحليل سورة", analysis["root_frequency"])
        tafsir_results.append({
            "text": ay["text"],
            "tafsir": tafsir
        })
    
    # 4) الاستدلال (نسخة مبسطة آمنة)
    full_text = " ".join([a["text"] for a in ayahs[:20]])
    try:
        # محاولة استخدام محرك الاستدلال الأصلي
        from utils.reasoning_engine import build_reasoning_path_v4
        reasoning = build_reasoning_path_v4(full_text[:500])
    except Exception as e:
        # في حال فشل، استخدم النسخة المبسطة
        reasoning = build_reasoning_fallback(full_text)
    
    return {
        "surah": surah_num,
        "roots": unique_roots[:20],
        "key_ayahs": key_ayahs,
        "tafsir": tafsir_results,
        "reasoning": reasoning
    }