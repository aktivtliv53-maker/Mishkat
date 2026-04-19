# ============================
#   Smart Dome Engine v4
#   متوافق مع Root Engine v7.0
# ============================

from utils.root_engine_v7 import analyze_text_v7

def build_smart_dome_v4(quran, surah_number):
    """بناء القبة الذكية للسورة"""
    surah_text = " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])
    analysis = analyze_text_v7(surah_text)
    
    return {
        "surah": surah_number,
        "roots": analysis["root_frequency"],
        "weights": analysis.get("root_weights", {}),
        "categories": analysis.get("root_categories", {}),
        "status": "Smart Dome v4 with Root Engine v7.0"
    }
