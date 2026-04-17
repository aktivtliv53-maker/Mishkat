import json
import re

BUCKWALTER = {
    'A': 'ا', 'b': 'ب', 't': 'ت', 'v': 'ث', 'j': 'ج',
    'H': 'ح', 'x': 'خ', 'd': 'د', '*': 'ذ', 'r': 'ر',
    'z': 'ز', 's': 'س', '$': 'ش', 'S': 'ص', 'D': 'ض',
    'T': 'ط', 'Z': 'ظ', 'E': 'ع', 'g': 'غ', 'f': 'ف',
    'q': 'ق', 'k': 'ك', 'l': 'ل', 'm': 'م', 'n': 'ن',
    'h': 'ه', 'w': 'و', 'y': 'ي', 'p': 'ة', 'Y': 'ى',
    "'": 'ء', '>': 'أ', '<': 'إ', '&': 'ؤ', '}': 'ئ',
    '|': 'آ', '`': 'ً', '~': 'ّ', 'F': 'ً', 'N': 'ٌ',
    'K': 'ٍ', 'a': 'َ', 'u': 'ُ', 'i': 'ِ', 'o': 'ْ'
}

def buckwalter_to_arabic(text):
    return ''.join(BUCKWALTER.get(c, c) for c in text)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def parse_corpus(filepath):
    word_root_map = {}
    
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("LOCATION"):
                continue
            
            # استخراج الجذر من حقل ROOT
            root_match = re.search(r'ROOT:([A-Za-z*><&}|\']+)', line)
            if not root_match:
                continue
            
            root_bw = root_match.group(1)
            root_arabic = buckwalter_to_arabic(root_bw)
            root_clean = normalize(root_arabic)
            
            # استخراج موقع الكلمة
            loc_match = re.match(r'\((\d+):(\d+):(\d+)', line)
            if not loc_match:
                continue
            
            surah = loc_match.group(1)
            ayah = loc_match.group(2)
            word_pos = loc_match.group(3)
            
            key = f"{surah}:{ayah}:{word_pos}"
            word_root_map[key] = root_clean
    
    return word_root_map

def main():
    print("جاري تحليل الملف...")
    word_root_map = parse_corpus("data/quran-morphology.txt")
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    # اختبار
    print("\nنماذج:")
    for key in list(word_root_map.items())[:10]:
        print(f"  {key[0]}: {key[1]}")
    
    json.dump(word_root_map, open("data/corpus_roots.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/corpus_roots.json")

main()