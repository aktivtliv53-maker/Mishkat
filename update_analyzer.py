import json
import re

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def build_word_to_root(quran, corpus_roots):
    """يبني خريطة كلمة ← جذر من الفهرس الموثوق"""
    word_root_map = {}
    
    for ayah in quran:
        s = ayah["surah_number"]
        a = ayah["ayah_number"]
        words = ayah["text"].split()
        
        for i, word in enumerate(words, 1):
            key = f"{s}:{a}:{i}"
            root = corpus_roots.get(key)
            if root:
                word_clean = normalize(word)
                word_root_map[word_clean] = root
    
    return word_root_map

def main():
    print("جاري البناء...")
    quran = load_json("data/matrix_data.json")
    corpus_roots = load_json("data/corpus_roots.json")
    
    word_root_map = build_word_to_root(quran, corpus_roots)
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    # اختبار
    test = ["الكتاب","للمتقين","يؤمنون","الغيب","الصلاة","الرحيم","رزقناهم","يعلمون","ذلك"]
    print("\nاختبار:")
    found = 0
    for word in test:
        r = word_root_map.get(normalize(word), "—")
        if r != "—":
            print(f"  ✓ {word} ← {r}")
            found += 1
        else:
            print(f"  ✗ {word}")
    
    print(f"\n{found}/{len(test)} ({found/len(test)*100:.1f}%)")
    
    json.dump(word_root_map, open("data/word_to_root.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/word_to_root.json")

main()