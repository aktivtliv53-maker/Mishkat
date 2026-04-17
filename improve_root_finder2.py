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

def deep_normalize(word):
    """تطبيع عميق للكلمة"""
    word = normalize(word)
    # حذف الألف المقصورة والممدودة في النهاية
    if word.endswith("اه") or word.endswith("اي"):
        word = word[:-1]
    # توحيد الواو والياء في وسط الكلمة
    return word

def build_roots_index(roots_data):
    index = {}
    for entry in roots_data:
        index[normalize(entry["root"])] = entry
    return index

def find_root_advanced(word, roots_index):
    word_clean = deep_normalize(word)
    
    if len(word_clean) < 2:
        return None

    # قائمة المرشحين
    candidates = set()
    candidates.add(word_clean)

    # البادئات
    prefixes = ["ال", "وال", "فال", "بال", "كال", "لل", "وب", "وف", "و", "ف", "ب", "ل", "س", "ك", "لي", "في"]
    for p in sorted(prefixes, key=len, reverse=True):
        if word_clean.startswith(p) and len(word_clean) > len(p) + 1:
            candidates.add(word_clean[len(p):])

    # اللواحق
    suffixes = ["تموه", "ناهم", "تموا", "هما", "هم", "كم", "هن", "نا", "ها", "وا", "ون", "ين", "ان", "ات", "تم", "تن", "ني", "وه", "يه", "ته", "ه", "ك", "ي", "ن", "ا"]
    
    new_candidates = set()
    for candidate in list(candidates):
        for s in sorted(suffixes, key=len, reverse=True):
            if candidate.endswith(s) and len(candidate) > len(s) + 1:
                new_candidates.add(candidate[:-len(s)])
    candidates.update(new_candidates)

    # حذف التضعيف
    more_candidates = set()
    for candidate in list(candidates):
        if len(candidate) >= 2 and candidate[-1] == candidate[-2]:
            more_candidates.add(candidate[:-1])
    candidates.update(more_candidates)

    # 1) بحث مباشر في المرشحين
    for candidate in sorted(candidates, key=len, reverse=True):
        if candidate in roots_index and len(candidate) >= 2:
            return roots_index[candidate]

    # 2) بحث جزئي — أفضل تطابق
    best_match = None
    best_len = 0
    for candidate in candidates:
        for root_clean, entry in roots_index.items():
            if len(root_clean) >= 3 and root_clean in candidate and len(root_clean) > best_len:
                best_match = entry
                best_len = len(root_clean)
    
    if best_match:
        return best_match

    # 3) بحث عكسي — الكلمة داخل الجذر الموسع
    for root_clean, entry in roots_index.items():
        if len(root_clean) >= 3:
            for candidate in candidates:
                if len(candidate) >= 3 and candidate in root_clean:
                    return entry

    return None

def test_finder(roots_index):
    test_words = [
        "ذلك", "الكتاب", "ريب", "فيه", "هدى", "للمتقين",
        "يؤمنون", "الغيب", "ويقيمون", "الصلاة", "مما", "رزقناهم", "ينفقون",
        "الرحمن", "الرحيم", "المتقين", "العالمين", "يعلمون", "كتبنا"
    ]
    
    print("اختبار الكاشف المحسّن v2:")
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