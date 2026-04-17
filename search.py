import json
import re
import os

def normalize(text):
    if not text:
        return ""
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def root_in_word(root, word):
    i = 0
    for char in word:
        if i < len(root) and char == root[i]:
            i += 1
    return i == len(root)

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "roots_mapped.json")

with open(path, encoding="utf-8") as f:
    data = json.load(f)

word_n = normalize("كتاب")
for entry in data:
    root_n = normalize(entry['root'])
    if root_in_word(root_n, word_n):
        print("تطابق:", entry['root'], "->", entry['ayah_count'], "آية")