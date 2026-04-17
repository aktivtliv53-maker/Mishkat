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

def main():
    print("جاري تحميل البيانات...")
    quran = load_json("data/matrix_data.json")
    ayah_roots = load_json("data/ayah_roots_index.json")
    roots_data = load_json("data/roots_mapped.json")
    
    roots_index = {normalize(r["root"]): r for r in roots_data}
    
    # بناء فهرس الآيات
    ayah_index = {}
    for ayah in quran:
        key = f"{ayah['surah_number']}:{ayah['ayah_number']}"
        ayah_index[key] = ayah
    
    print("جاري بناء فهرس الكلمات...")
    
    word_root_map = {}
    
    for ayah_key, roots in ayah_roots.items():
        ayah = ayah_index.get(ayah_key)
        if not ayah:
            continue
        
        words = ayah["text"].split()
        
        for word in words:
            word_clean = normalize(word)
            if len(word_clean) < 2:
                continue
            
            # جرب كل جذر من جذور هذه الآية
            best_root = None
            best_score = 0
            
            for root in roots:
                root_clean = normalize(root)
                if root_clean in word_clean:
                    score = len(root_clean)
                    if score > best_score:
                        best_score = score
                        best_root = root_clean
            
            if best_root:
                word_root_map[word_clean] = best_root
    
    print(f"عدد الكلمات المفهرسة: {len(word_root_map)}")
    
    # اختبار
    test = [
        "الكتاب", "للمتقين", "يؤمنون", "الغيب",
        "ويقيمون", "الصلاة", "الرحيم", "ذلك"
    ]
    
    print("\nاختبار:")
    print("="*50)
    found = 0
    for word in test:
        word_clean = normalize(word)
        root = word_root_map.get(word_clean)
        if root and root in roots_index:
            entry = roots_index[root]
            print(f"✓ {word} ← {entry['root']} ({entry.get('meanings','')})")
            found += 1
        else:
            print(f"✗ {word}")
    
    print(f"\nنسبة النجاح: {found}/{len(test)} ({found/len(test)*100:.1f}%)")
    
    with open("data/word_root_final.json", "w", encoding="utf-8") as f:
        json.dump(word_root_map, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم الحفظ في data/word_root_final.json")

main()