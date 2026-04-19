# ============================
#   Fusion Engine v7 — Final
#   متوافق مع Root Engine v7
#   بدون root_canonizer
# ============================

from utils.root_engine_v7 import analyze_text_v7
from utils.surah_map_engine import get_surah_roots_v7, get_surah_stats_v7
from utils.mesh_engine import build_mesh_networks_v3

def run_full_analysis(quran, surah_number):
    """
    دمج جميع المحركات:
    - Root Engine v7
    - Surah Map v7
    - Mesh Networks v3
    """

    # 1) تحليل الجذور للنص الكامل للسورة
    surah_stats = get_surah_stats_v7(quran, surah_number)

    # 2) شبكة الجذور (Mesh)
    mesh = build_mesh_networks_v3(quran, surah_number)

    # 3) جذور السورة (قائمة مرتبة)
    roots = get_surah_roots_v7(quran, surah_number)

    return {
        "surah": surah_number,
        "roots": roots,
        "stats": surah_stats,
        "mesh": mesh,
        "status": "Fusion Engine v7 — Fully Operational"
    }
