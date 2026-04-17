# utils/smart_dome_engine.py — v11.3 (Smart Dome v4)

from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root

def build_smart_dome_v4(quran, surah_number):
    text = " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])
    analysis = analyze_text_v5(text)

    freq = {}
    for root, count in analysis["root_frequency"]:
        canon = canonize_root(root)
        freq[canon] = freq.get(canon, 0) + count

    freq_sorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    ayat = [a for a in quran if a["surah_number"] == surah_number]
    center_ayah = ayat[len(ayat)//2] if ayat else None

    return {
        "surah": surah_number,
        "unique_roots": len(freq_sorted),
        "top_roots": freq_sorted[:20],
        "center_ayah": center_ayah,
        "status": "Smart Dome v4 built"
    }