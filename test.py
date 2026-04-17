import json
import re

ROOTS_FILE = "data/roots_mapped.json"
WORD_INDEX_FILE = "data/word_to_root.json"

def normalize(text):
    if not text:
        return ""
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱؤئ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def load_db():
    with open(ROOTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return {normalize(entry["root"]): entry for entry in data}

def load_word_index():
    with open(WORD_INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)

def search(word):
    db = load_db()
    word_index = load_word_index()
    word_clean = normalize(word)

    root = word_index.get(word_clean)

    if not root:
        prefixes = ["ال", "و", "ف", "ب", "ل", "س", "ك"]
        for p in prefixes:
            if word_clean.startswith(p):
                candidate = word_clean[len(p):]
                root = word_index.get(candidate)
                if root:
                    break

    if not root:
        print(f"لم يُعثر على جذر للكلمة: {word}")
        return

    root_clean = normalize(root)
    entry = db.get(root_clean)

    if not entry:
        print(f"الجذر '{root}' غير موجود في القاعدة")
        return

    print(f"الكلمة: {word}")
    print(f"الجذر: {entry['root']}")
    print(f"المعنى: {entry['meanings']}")
    print(f"عدد الآيات: {entry['ayah_count']}")
    print(f"أول آية: {entry['ayahs'][0]['text'] if entry['ayahs'] else 'لا يوجد'}")
    print("---")

search("كتاب")
search("الرحمة")
search("العدل")
search("يكتبون")