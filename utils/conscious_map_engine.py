# ============================
#   Conscious Map Engine v1
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.root_canonizer import canonize_root

def build_conscious_map(surah_num, quran):
    """بناء خريطة واعية للسورة"""
    ayahs = [a for a in quran if a["surah_number"] == surah_num]
    full_text = " ".join([a["text"] for a in ayahs])
    
    analysis = analyze_text_v7(full_text)
    
    # الآيات المحورية (أعلى 5 آيات من حيث عدد الجذور)
    scored_ayahs = []
    for ayah in ayahs:
        ayah_analysis = analyze_text_v7(ayah["text"])
        scored_ayahs.append((ayah, len(ayah_analysis["root_frequency"])))
    
    scored_ayahs.sort(key=lambda x: x[1], reverse=True)
    key_ayahs = [a for a, _ in scored_ayahs[:5]]
    
    return {
        "surah": surah_num,
        "roots": [r for r, _ in analysis["root_frequency"]],
        "key_ayahs": key_ayahs,
        "status": "Conscious Map v1 with Root Engine v7.0"
    }
