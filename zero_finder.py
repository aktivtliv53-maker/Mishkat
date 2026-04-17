import json
import re

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def build_index(roots_data):
    index = {}
    for entry in roots_data:
        root_clean = normalize(entry["root"])
        for ayah in entry.get("ayahs", []):
            for word in ayah["text"].split():
                word_clean = normalize(word)
                if word_clean not in index:
                    index[word_clean] = entry
    return index

def main():
    roots_data = json.load(open("data/roots_mapped.json", encoding="utf-8"))
    print("جاري البناء...")
    index = build_index(roots_data)
    print(f"عدد الكلمات: {len(index)}")
    
    test = ["الكتاب","للمتقين","يؤمنون","الغيب","الصلاة","الرحيم","رزقناهم","يعلمون"]
    found = 0
    for word in test:
        r = index.get(normalize(word))
        if r:
            print(f"✓ {word} ← {r['root']} ({r.get('meanings','')})")
            found += 1
        else:
            print(f"✗ {word}")
    
    print(f"\n{found}/{len(test)} ({found/len(test)*100:.1f}%)")
    
    # حفظ
    output = {k: {"root": v["root"], "meanings": v.get("meanings","")} for k,v in index.items()}
    json.dump(output, open("data/word_index.json","w", encoding="utf-8"), ensure_ascii=False)
    print("✅ data/word_index.json")

main()