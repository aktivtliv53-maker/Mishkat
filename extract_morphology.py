import json
import re
from collections import Counter

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def find_extra_letters(word, root):
    """يجد الحروف الزائدة في الكلمة عن الجذر"""
    word = normalize(word)
    root = normalize(root)
    
    extra_start = []
    extra_end = []
    
    # حروف زائدة في البداية
    for i in range(1, len(word)):
        prefix = word[:i]
        remaining = word[i:]
        if root in remaining or remaining.startswith(root[:2]):
            extra_start = list(prefix)
            break
    
    # حروف زائدة في النهاية
    for i in range(len(word)-1, 0, -1):
        suffix = word[i:]
        remaining = word[:i]
        if root in remaining or remaining.endswith(root[-2:]):
            extra_end = list(suffix)
            break
    
    return extra_start, extra_end

def analyze_letter_morphology(letter, roots_data, quran_data):
    """يحلل الدور الصرفي لحرف معين كحرف زائد"""
    
    letter = normalize(letter)
    patterns_start = Counter()
    patterns_end = Counter()
    examples_start = []
    examples_end = []

    for entry in roots_data:
        root = normalize(entry["root"])
        if letter in root:
            continue  # نتجاهل الحروف الأصلية
        
        for ayah in entry.get("ayahs", [])[:5]:
            words = normalize(ayah["text"]).split()
            for word in words:
                if len(word) < 3:
                    continue
                if root not in word:
                    continue
                    
                extra_start, extra_end = find_extra_letters(word, root)
                
                if letter in extra_start:
                    pattern = f"{''.join(extra_start)}-{root}"
                    patterns_start[pattern] += 1
                    if len(examples_start) < 5:
                        examples_start.append({
                            "word": word,
                            "root": root,
                            "pattern": pattern,
                            "ayah": ayah["text"][:50]
                        })
                
                if letter in extra_end:
                    pattern = f"{root}-{''.join(extra_end)}"
                    patterns_end[pattern] += 1
                    if len(examples_end) < 5:
                        examples_end.append({
                            "word": word,
                            "root": root,
                            "pattern": pattern,
                            "ayah": ayah["text"][:50]
                        })

    return {
        "letter": letter,
        "patterns_start": dict(patterns_start.most_common(10)),
        "patterns_end": dict(patterns_end.most_common(10)),
        "examples_start": examples_start,
        "examples_end": examples_end
    }

def main():
    print("جاري تحميل البيانات...")
    roots_data = load_json("data/roots_mapped.json")
    quran_data = load_json("data/matrix_data.json")
    
    letter = input("أدخل الحرف: ").strip()
    
    print(f"جاري تحليل الدور الصرفي للحرف: {letter}")
    result = analyze_letter_morphology(letter, roots_data, quran_data)
    
    print(f"\n{'='*50}")
    print(f"الحرف: {letter}")
    print(f"\nأنماط الزيادة في البداية:")
    for p, c in result["patterns_start"].items():
        print(f"  {p}: {c} مرة")
    
    print(f"\nأنماط الزيادة في النهاية:")
    for p, c in result["patterns_end"].items():
        print(f"  {p}: {c} مرة")
    
    print(f"\nأمثلة من البداية:")
    for e in result["examples_start"][:3]:
        print(f"  {e['word']} ← جذر {e['root']}")
    
    print(f"\nأمثلة من النهاية:")
    for e in result["examples_end"][:3]:
        print(f"  {e['word']} ← جذر {e['root']}")
    
    output = f"data/morphology_{letter}.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ تم الحفظ في {output}")

main()