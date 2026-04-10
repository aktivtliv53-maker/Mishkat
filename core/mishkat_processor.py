import re
import json
import os

# ---------------------------------------------------------
# تحميل قاعدة البيانات
# ---------------------------------------------------------
_DB = None

def _load_db():
    global _DB
    if _DB is not None:
        return _DB
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "data", "roots_mapped.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _DB = {entry["root"]: entry for entry in data}
    return _DB

# ---------------------------------------------------------
# 1) تطبيع النص العربي
# ---------------------------------------------------------
def normalize(text):
    if not text:
        return ""
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

# ---------------------------------------------------------
# 2) البحث عن جذر كلمة في القاعدة
# ---------------------------------------------------------
def find_root(word):
    db = _load_db()
    word_clean = normalize(word)
    prefixes = ["ال", "و", "ف", "ب", "ل", "س", "ك"]
    candidates = [word_clean]
    for p in prefixes:
        if word_clean.startswith(p) and len(word_clean) > len(p) + 1:
            candidates.append(word_clean[len(p):])
    for candidate in candidates:
        for root in db:
            if normalize(root) == candidate:
                return root
    return None

# ---------------------------------------------------------
# 3) استخراج بيانات جذر كامل
# ---------------------------------------------------------
def get_root_data(word):
    db = _load_db()
    root = find_root(word)
    if not root:
        return None
    return db.get(root)

# ---------------------------------------------------------
# 4) تحليل نص كامل
# ---------------------------------------------------------
def process_text(text):
    if not isinstance(text, str):
        return {}

    words = text.split()
    results = []
    all_ayahs = {}

    for word in words:
        data = get_root_data(word)
        if data:
            results.append({
                "word": word,
                "root": data["root"],
                "meanings": data["meanings"],
                "ayah_count": data["ayah_count"]
            })
            for ayah in data["ayahs"]:
                key = ayah["index"]
                if key not in all_ayahs:
                    all_ayahs[key] = ayah

    return {
        "raw_text": text,
        "words_analyzed": results,
        "total_ayahs": len(all_ayahs),
        "ayahs": sorted(all_ayahs.values(), key=lambda x: x["index"])
    }

# ---------------------------------------------------------
# 5) بناء شبكة الجذور للعرض البصري
# ---------------------------------------------------------
def build_root_graph(text):
    words = text.split()
    nodes = []
    edges = []
    seen = set()
    last_root = None

    for word in words:
        data = get_root_data(word)
        if not data:
            continue
        root = data["root"]
        if root not in seen:
            nodes.append({
                "id": root,
                "label": root,
                "meanings": data["meanings"],
                "ayah_count": data["ayah_count"]
            })
            seen.add(root)
        if last_root and last_root != root:
            edges.append({
                "source": last_root,
                "target": root,
                "weight": 1
            })
        last_root = root

    return nodes, edges
