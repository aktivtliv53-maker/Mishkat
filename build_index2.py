import json
import re

CORPUS_FILE = "data/quranic-corpus-morphology-0.4.txt"
OUTPUT_FILE = "data/word_to_root.json"

BUCKWALTER = {
    'a': '', 'A': 'ا', 'b': 'ب', 't': 'ت', 'v': 'ث',
    'j': 'ج', 'H': 'ح', 'x': 'خ', 'd': 'د', '*': 'ذ',
    'r': 'ر', 'z': 'ز', 's': 'س', '$': 'ش', 'S': 'ص',
    'D': 'ض', 'T': 'ط', 'Z': 'ظ', 'E': 'ع', 'G': 'غ',
    'g': 'غ', 'f': 'ف', 'q': 'ق', 'k': 'ك', 'l': 'ل',
    'm': 'م', 'n': 'ن', 'h': 'ه', 'w': 'و', 'y': 'ي',
    'p': 'ة', 'Y': 'ى', "'": 'أ', '{': 'إ', '&': 'ؤ',
    '<': 'إ', '>': 'أ', '|': 'آ', '`': 'ء', 'W': 'و',
    'o': '', 'u': '', 'i': '', '~': '', 'F': '',
    'N': '', 'K': '', 'U': '', 'I': '', 'e': ''
}

def bw(text):
    return "".join(BUCKWALTER.get(c, '') for c in text)

def normalize(text):
    if not text:
        return ""
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱؤئ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

word_to_root = {}

with open(CORPUS_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        word = normalize(bw(parts[1])) if len(parts) > 1 else ""
        morphology = parts[3]
        root_match = re.search(r"ROOT:([^\|]+)", morphology)
        if not root_match or not word:
            continue
        root = normalize(bw(root_match.group(1)))
        if word and root:
            word_to_root[word] = root

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(word_to_root, f, ensure_ascii=False, indent=2)

print(f"✅ تم بناء فهرس {len(word_to_root)} كلمة")
print("عينة:")
for k, v in list(word_to_root.items())[:5]:
    print(f"  {k} -> {v}")