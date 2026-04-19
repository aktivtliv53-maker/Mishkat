# ============================
#   Fusion Engine v7 — Unified Analysis Layer
#   (متوافق مع Surah Map v7 الجديدة)
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.surah_map_engine import build_surah_map
from utils.conscious_map_engine import build_conscious_map

# ------------------------------------
# 1) التحليل الكامل للنص
# ------------------------------------
def run_full_analysis(quran, surah_number, text=None):
    result = {}

    # -----------------------------
    # A) تحليل الجذور للنص الحر
    # -----------------------------
    if text:
        result["text_root_analysis"] = analyze_text_v7(text)

    # -----------------------------
    # B) خريطة السورة (شبكة جذور)
    # -----------------------------
    surah_map = build_surah_map(quran, surah_number)
    result["surah_nodes"] = surah_map["nodes"]
    result["surah_links"] = surah_map["links"]

    # -----------------------------
    # C) الخريطة الواعية (جذور سيادية)
    # -----------------------------
    conscious = build_conscious_map(quran, surah_number)
    result["conscious_levels"] = conscious["levels"]

    # -----------------------------
    # D) إحصاءات عامة
    # -----------------------------
    result["stats"] = {
        "unique_roots": len(surah_map["nodes"]),
        "connections": len(surah_map["links"]),
        "sovereign_roots": len(conscious["levels"])
    }

    return result
