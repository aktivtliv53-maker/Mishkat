# ============================
#   Mishkat Ayah Matcher v1.0
#   (Semantic Matching)
# ============================

def match_ayahs_by_roots(roots, quran, top_n=10):
    """مطابقة الآيات بناءً على الجذور مع تحديد عدد النتائج"""
    results = []
    for ayah in quran:
        text = ayah.get("text", "")
        score = 0
        for root in roots:
            if root and root in text:
                score += 1
        if score > 0:
            results.append({
                "surah_number": ayah.get("surah_number"),
                "ayah_number": ayah.get("ayah_number"),
                "text": text,
                "score": score
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]