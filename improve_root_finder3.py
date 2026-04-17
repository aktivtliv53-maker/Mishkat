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

def build_word_root_map(ayah_roots_index, quran_data):
    """يبني خريطة كلمة ← جذر من الآيات والجذور المعروفة"""
    
    # فهرس الآيات
    ayah_index = {}
    for ayah in quran_data:
        key = f"{ayah['surah_number']}:{ayah['ayah_number']}"
        ayah_index[key] = ayah
    
    word_root_map = {}
    
    for ayah_key, roots in ayah_roots_index.items():
        ayah = ayah_index.get(ayah_key)
        if not ayah:
            continue
        
        words = ayah["text"].split()
        words_clean = [normalize(w) for w in words]
        
        for root in roots:
            root_clean = normalize(root)
            for word_clean in words_clean:
                if len(word_clean) < 2:
                    continue
                # الجذر موجود في الكلمة
                if root_clean in word_clean:
                    if word_clean not in word_root_map:
                        word_root_map[word_clean] = root_clean
    
    return word_root_map

def find_root_with_map(word, word_root_map, roots_index):
    word_clean = normalize(word)
    
    # 1) بحث مباشر في الخريطة
    if word_clean in word_root_map:
        root = word_root_map[word_clean]
        if root in roots_index:
            return roots_index[root]
    
    # 2) بحث بعد حذف البادئات
    prefixes = ["ال", "وال", "فال", "بال", "لل", "و", "ف", "ب", "ل", "س", "ك"]
    for p in sorted(prefixes, key=len, reverse=True):
        if word_clean.startswith(p):
            candidate = word_clean[len(p):]
            if candidate in word_root_map:
                root = word_root_map[candidate]
                if root in roots_index:
                    return roots_index[root]
    
    # 3) بحث بعد حذف اللواحق
    suffixes = ["هم", "كم", "هن", "نا", "ها", "وا", "ون", "ين", "ان", "ات", "تم", "ه", "ك", "ي", "ن", "ا"]
    for s in sorted(suffixes, key=len, reverse=True):
        if word_clean.endswith(s) and len(word_clean) > len(s) + 1:
            candidate = word_clean[:-len(s)]
            if candidate in word_root_map:
                root = word_root_map[candidate]
                if root in roots_index:
                    return roots_index[root]
    
    # 4) بحث في قاموس الجذور مباشرة
    if word_clean in roots_index:
        return roots_index[word_clean]
    
    return None

def test_finder(word_root_map, roots_index):
    test_words = [
        "ذلك", "الكتاب", "ريب", "فيه", "هدى", "للمتقين",
        "يؤمنون", "الغيب", "ويقيمون", "الصلاة", "مما",
        "رزقناهم", "ينفقون", "الرحمن", "الرحيم", "يعلمون", "كتبنا"
    ]
    
    print("اختبار الكاشف v3 (مبني على الآيات):")
    print("="*55)
    found = 0
    for word in test_words:
        result = find_root_with_map(word, word_root_map, roots_index)
        if result:
            print(f"✓ {word} ← {result['root']} ({result.get('meanings', '')})")
            found += 1
        else:
            print(f"✗ {word} — لم يُعثر على جذر")
    
    print(f"\nنسبة النجاح: {found}/{len(test_words)} ({found/len(test_words)*100:.1f}%)")

def main():
    print("جاري تحميل البيانات...")
    quran_data = load_json("data/matrix_data.json")
    roots_data = load_json("data/roots_mapped.json")
    ayah_roots = load_json("data/ayah_roots_index.json")
    
    roots_index = {normalize(r["root"]): r for r in roots_data}
    
    print("جاري بناء خريطة الكلمات...")
    word_root_map = build_word_root_map(ayah_roots, quran_data)
    print(f"عدد الكلمات في الخريطة: {len(word_root_map)}")
    
    test_finder(word_root_map, roots_index)
    
    # حفظ الخريطة
    with open("data/word_root_map.json", "w", encoding="utf-8") as f:
        json.dump(word_root_map, f, ensure_ascii=False, indent=2)
    print(f"\n✅ تم الحفظ في data/word_root_map.json")

main()