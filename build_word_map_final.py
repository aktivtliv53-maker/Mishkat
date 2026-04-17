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

def build_final_map(ayah_roots, quran_data):
    ayah_index = {}
    for ayah in quran_data:
        key = f"{ayah['surah_number']}:{ayah['ayah_number']}"
        ayah_index[key] = ayah

    word_root_map = {}

    for ayah_key, roots in ayah_roots.items():
        ayah = ayah_index.get(ayah_key)
        if not ayah:
            continue

        words = ayah["text"].split()
        
        for root in roots:
            root_clean = normalize(root)
            
            for word in words:
                word_clean = normalize(word)
                if len(word_clean) < 2:
                    continue
                
                # الجذر موجود في الكلمة
                if root_clean in word_clean:
                    word_root_map[word_clean] = root_clean
                    
                    # أيضاً نضيف بعد حذف البادئات
                    for p in ["ال", "وال", "فال", "بال", "لل", "و", "ف", "ب", "ل"]:
                        if word_clean.startswith(p):
                            stripped = word_clean[len(p):]
                            if root_clean in stripped:
                                word_root_map[stripped] = root_clean

    return word_root_map

def find_root(word, word_root_map, roots_index):
    word_clean = normalize(word)
    
    # بحث مباشر
    if word_clean in word_root_map:
        root = word_root_map[word_clean]
        return roots_index.get(root)
    
    # حذف البادئات
    prefixes = ["ال", "وال", "فال", "بال", "لل", "و", "ف", "ب", "ل", "س", "ك"]
    for p in sorted(prefixes, key=len, reverse=True):
        if word_clean.startswith(p):
            candidate = word_clean[len(p):]
            if candidate in word_root_map:
                root = word_root_map[candidate]
                return roots_index.get(root)
    
    # حذف اللواحق
    suffixes = ["هم", "كم", "هن", "نا", "ها", "وا", "ون", "ين", "ان", "ات", "تم", "ه", "ك", "ي", "ن"]
    for s in sorted(suffixes, key=len, reverse=True):
        if word_clean.endswith(s) and len(word_clean) > len(s) + 1:
            candidate = word_clean[:-len(s)]
            if candidate in word_root_map:
                root = word_root_map[candidate]
                return roots_index.get(root)
            # بحث بعد حذف البادئة واللاحقة معاً
            for p in sorted(prefixes, key=len, reverse=True):
                if candidate.startswith(p):
                    c2 = candidate[len(p):]
                    if c2 in word_root_map:
                        root = word_root_map[c2]
                        return roots_index.get(root)
    
    return None

def main():
    print("جاري تحميل البيانات...")
    quran_data = load_json("data/matrix_data.json")
    roots_data = load_json("data/roots_mapped.json")
    ayah_roots = load_json("data/ayah_roots_index.json")
    
    roots_index = {normalize(r["root"]): r for r in roots_data}
    
    print("جاري بناء الخريطة...")
    word_root_map = build_final_map(ayah_roots, quran_data)
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    # اختبار
    test_words = [
        "ذلك", "الكتاب", "ريب", "فيه", "هدى", "للمتقين",
        "يؤمنون", "الغيب", "ويقيمون", "الصلاة",
        "رزقناهم", "ينفقون", "الرحمن", "الرحيم", "يعلمون"
    ]
    
    print("\nاختبار:")
    print("="*50)
    found = 0
    for word in test_words:
        result = find_root(word, word_root_map, roots_index)
        if result:
            print(f"✓ {word} ← {result['root']} ({result.get('meanings', '')})")
            found += 1
        else:
            print(f"✗ {word}")
    
    print(f"\nنسبة النجاح: {found}/{len(test_words)} ({found/len(test_words)*100:.1f}%)")
    
    with open("data/word_root_map_final.json", "w", encoding="utf-8") as f:
        json.dump(word_root_map, f, ensure_ascii=False, indent=2)
    print(f"\n✅ تم الحفظ في data/word_root_map_final.json")

main()