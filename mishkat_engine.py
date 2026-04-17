import json
import re
from collections import defaultdict

# -----------------------------
# تحميل القرآن من quran.json
# -----------------------------
def load_quran():
    with open("data/quran.json", encoding="utf-8") as f:
        return json.load(f)

QURAN = load_quran()

# -----------------------------
# بناء خريطة الكلمات → الجذور
# -----------------------------
def normalize(word):
    word = re.sub(r"[ًٌٍَُِّْـٰ]", "", word)
    word = re.sub(r"[أإآٱ]", "ا", word)
    word = word.replace("ة", "ه").replace("ى", "ي")
    return word.strip()

def find_root(word):
    """إرجاع الكلمة نفسها كجذر مبسط (placeholder)"""
    return normalize(word)

def build_corpus_word_map():
    mapping = defaultdict(list)

    for ayah in QURAN:
        surah = ayah["surah_number"]
        num = ayah["ayah_number"]
        text = ayah["text"]

        words = text.split()
        for w in words:
            root = find_root(w)
            mapping[root].append({
                "surah": surah,
                "ayah_number": num,
                "text": text
            })

    return mapping

CORPUS_WORD_MAP = build_corpus_word_map()