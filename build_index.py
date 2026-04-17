import json
import re

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def main():
    print("جاري التحميل...")
    roots_data = json.load(open("data/roots_mapped.json", encoding="utf-8"))
    
    word_root_map = {}
    
    for entry in roots_data:
        root_clean = normalize(entry["root"])
        for ayah in entry.get("ayahs", []):
            for word in ayah["text"].split():
                word_clean = normalize(word)
                if root_clean in word_clean and len(root_clean) >= 2:
                    if word_clean not in word_root_map:
                        word_root_map[word_clean] = root_clean

    print(f"عدد الكلمات: {len(word_root_map)}")
    
    test = ["الكتاب","للمتقين","يؤمنون","الغيب","الصلاة","الرحيم","رزقناهم","يعلمون"]
    print("\nاختبار:")
    for word in test:
        r = word_root_map.get(normalize(word), "✗")
        print(f"  {word}: {r}")
    
    json.dump(word_root_map, open("data/word_root_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/word_root_map.json")

main()