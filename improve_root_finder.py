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

def build_roots_index(roots_data):
    index = {}
    for entry in roots_data:
        index[normalize(entry["root"])] = entry
    return index

def find_root_advanced(word, roots_index):
    word_clean = normalize(word)
    
    if len(word_clean) < 2:
        return None

    # 1) مطابقة مباشرة
    if word_clean in roots_index:
        return roots_index[word_clean]

    # 2) حذف البادئات
    prefixes = ["ال", "وال", "فال", "بال", "كال", "لل", "و", "ف", "ب", "ل", "س", "ك"]
    for p in sorted(prefixes, key=len, reverse=True):
        if word_clean.startswith(p):
            candidate = word_clean[len(p):]
            if candidate in roots_index:
                return roots_index[candidate]

    # 3) حذف اللواحق
    suffixes = ["هم", "كم", "هن", "نا", "ها", "وا", "ون", "ين", "ان", "ات", "تم", "تن", "ني", "ه", "ك", "ي", "ن"]
    for s in sorted(suffixes, key=len, reverse=True):
        if word_clean.endswith(s) and len(word_clean) > len(s) + 1:
            candidate = word_clean[:-len(s)]
            if candidate in roots_index:
                return roots_index[candidate]

    # 4) حذف بادئة ولاحقة معاً
    for p in sorted(prefixes, key=len, reverse=True):
        if word_clean.startswith(p):
            stripped = word_clean[len(p):]
            for s in sorted(suffixes, key=len, reverse=True):
                if stripped.endswith(s) and len(stripped) > len(s) + 1:
                    candidate = stripped[:-len(s)]
                    if candidate in roots_index:
                        return roots_index[candidate]

    # 5) بحث جزئي — الجذر موجود داخل الكلمة
    best_match = None
    best_len = 0
    for root_clean, entry in roots_index.items():
        if len(root_clean) >= 3 and root_clean in word_clean:
            if len(root_clean) > best_len:
                best_match = entry
                best_len = len(root_clean)
    
    if best_match:
        return best_match

    return None

def test_finder(roots_index):
    """اختبار على آية البقرة 2"""
    test_words = [
        "ذلك", "الكتاب", "ريب", "فيه", "هدى", "للمتقين",
        "يؤمنون", "الغيب", "ويقيمون", "الصلاة", "مما", "رزقناهم", "ينفقون"
    ]
    
    print("اختبار الكاشف المحسّن:")
    print("="*50)
    found = 0
    for word in test_words:
        result = find_root_advanced(word, roots_index)
        if result:
            print(f"✓ {word} ← {result['root']} ({result.get('meanings', '')})")
            found += 1
        else:
            print(f"✗ {word} — لم يُعثر على جذر")
    
    print(f"\nنسبة النجاح: {found}/{len(test_words)} ({found/len(test_words)*100:.1f}%)")

def main():
    print("جاري تحميل البيانات...")
    roots_data = load_json("data/roots_mapped.json")
    roots_index = build_roots_index(roots_data)
    print(f"عدد الجذور: {len(roots_index)}")
    
    test_finder(roots_index)

main()