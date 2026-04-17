import streamlit as st

from utils.semantic_engine import (
    get_similar_ayahs,
    extract_roots_from_matches
)
from utils.reasoning_engine import (
    explain_ayah_similarity
)
from utils.data_loader import load_quran


class MishkatBrain:
    def __init__(self):
        self.quran = load_quran()

    def think(self, query):
        """المسار الكامل للتفكير في Mishkat v9.1"""

        result = {
            "query": query,
            "roots": [],
            "surahs": [],
            "answer": "",
            "ayahs": [],
            "guidance": []
        }

        # 1) أقرب الآيات
        matches = get_similar_ayahs(query, top_k=10)

        result["ayahs"] = [
            {
                "text": self.quran[idx]["text"],
                "surah": self.quran[idx]["surah_number"],
                "ayah": self.quran[idx]["ayah_number"]
            }
            for idx, _ in matches
        ]

        # 2) استخراج الجذور
        roots = extract_roots_from_matches(matches)
        result["roots"] = [r for r, _ in roots[:5]]

        # 3) السور الأقرب
        surah_counts = {}
        for idx, _ in matches:
            s = self.quran[idx]["surah_number"]
            surah_counts[s] = surah_counts.get(s, 0) + 1

        result["surahs"] = sorted(
            surah_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # 4) الجواب الذكي
        result["answer"] = explain_ayah_similarity(query, matches)

        # 5) مسار الهداية
        result["guidance"] = [
            {"title": "تأمل", "text": "اقرأ الآيات ببطء وتأمل معانيها."},
            {"title": "تتبع", "text": "لاحظ الجذور المشتركة بين الآيات."},
            {"title": "اربط", "text": "اربط السور ببعضها لفهم السياق الكامل."}
        ]

        return result


# ============================
#   النسخة المطلوبة: get_brain()
# ============================
@st.cache_resource
def get_brain():
    return MishkatBrain()