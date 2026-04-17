import json
import re
from collections import defaultdict


# ============================================================
# 1. تحميل البيانات
# ============================================================

def load_roots_mapped(path='data/roots_mapped.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_word_to_root(path='data/word_to_root.json'):
    """تحميل القاموس الجاهز: كلمة -> جذر"""
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ============================================================
# 2. أدوات النص
# ============================================================

def remove_tashkeel(text):
    """إزالة التشكيل من النص"""
    return re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670\u0640]', '', text)

def normalize_word(word):
    """
    تنظيف الكلمة للبحث:
    والكتاب -> كتاب
    بالعلم -> علم
    """
    # إزالة الواو والفاء أولاً
    while len(word) > 2 and word[0] in 'وف':
        word = word[1:]

    # قاعدة واحدة فقط حسب البداية
    if word.startswith('ال') and len(word) > 3:
        return word[2:]
    elif len(word) > 3 and word[0] in 'بلك' and word[1:3] == 'ال':
        return word[3:]
    elif len(word) > 3 and word[0] in 'بلك' and word[1] != 'ا':
        return word[1:]

    return word

def normalize_hamza(word):
    """توحيد الهمزات — أ إ آ ء -> ا"""
    return re.sub(r'[أإآء]', 'ا', word)

def find_root(word, word_to_root):
    """
    يبحث عن جذر الكلمة بأربع خطوات:
    1. الكلمة كما هي
    2. بعد إزالة التشكيل
    3. بعد التطبيع الكامل
    4. بعد توحيد الهمزات
    """
    if word in word_to_root:
        return word_to_root[word]
    clean = remove_tashkeel(word)
    if clean in word_to_root:
        return word_to_root[clean]
    normalized = normalize_word(clean)
    if normalized in word_to_root:
        return word_to_root[normalized]
    no_hamza = normalize_hamza(normalized)
    if no_hamza in word_to_root:
        return word_to_root[no_hamza]
    return None


# ============================================================
# 3. البحث عن بيانات جذر
# ============================================================

def get_root_data(root, roots_mapped):
    """إرجاع كل بيانات جذر معين من roots_mapped"""
    for entry in roots_mapped:
        if entry['root'] == root:
            return entry
    return None


# ============================================================
# 4. استخلاص المفهوم من تقاطع السياقات
# ============================================================

def extract_concept(root_data):
    if not root_data:
        return None

    ayahs = root_data.get('ayahs', [])
    root = root_data['root']

    surah_spread = defaultdict(list)
    for ayah in ayahs:
        surah_spread[ayah['surah']].append(ayah['text'])

    companion_words = defaultdict(int)
    stop_words = {
        'في', 'من', 'إلى', 'على', 'عن', 'مع', 'هو', 'هي', 'هم', 'هن',
        'أن', 'إن', 'لا', 'ما', 'و', 'ف', 'ب', 'ل', 'ك',
        'كان', 'قال', 'يكون', 'قالوا', 'كانوا', 'يقول',
        'ذلك', 'هذا', 'هذه', 'تلك', 'التي', 'الذي', 'الذين',
        'كل', 'قد', 'لم', 'لن', 'إلا', 'أو', 'ثم', 'حتى',
        'الله', 'رب', 'إنه', 'إنا', 'إنهم', 'وما', 'وإن',
    }

    for ayah in ayahs:
        clean = remove_tashkeel(ayah['text'])
        words = re.findall(r'[\u0621-\u064A]+', clean)
        for word in words:
            w = normalize_word(word)
            if w not in stop_words and w != root and len(w) > 2:
                companion_words[w] += 1

    top_companions = sorted(companion_words.items(),
                            key=lambda x: x[1], reverse=True)[:20]

    return {
        'root': root,
        'total_ayahs': root_data['ayah_count'],
        'surah_count': len(surah_spread),
        'surahs': dict(surah_spread),
        'top_companions': top_companions,
        'all_ayahs': ayahs
    }


# ============================================================
# 5. تحليل نص خارجي
# ============================================================

def analyze_text(text, roots_mapped, word_to_root):
    clean = remove_tashkeel(text)
    raw_words = re.findall(r'[\u0621-\u064A]+', clean)

    results = {}
    not_found = []

    for raw_word in raw_words:
        if raw_word in results:
            continue

        root = find_root(raw_word, word_to_root)

        if root:
            root_data = get_root_data(root, roots_mapped)
            concept = extract_concept(root_data)
            results[raw_word] = {
                'word': raw_word,
                'root': root,
                'concept': concept
            }
        else:
            not_found.append(raw_word)

    return {
        'original_text': text,
        'analyzed_words': results,
        'not_found': not_found,
        'total_words': len(raw_words),
        'matched_words': len(results)
    }


# ============================================================
# 6. توليد ملخص للعرض
# ============================================================

def summarize_concept(concept):
    if not concept:
        return "لم يُعثر على بيانات لهذا الجذر."

    root = concept['root']
    total = concept['total_ayahs']
    surah_count = concept['surah_count']
    companions = [w for w, _ in concept['top_companions'][:10]]
    surahs = list(concept['surahs'].keys())

    return f"""الجذر: {root}
━━━━━━━━━━━━━━━━━━━━━━━
ورد في: {total} آية | في {surah_count} سورة
السور: {' ، '.join(surahs[:10])}{'...' if surah_count > 10 else ''}
الكلمات المرافقة: {' ، '.join(companions)}"""


# ============================================================
# 7. الدالة الرئيسية
# ============================================================

def process(input_text,
            roots_mapped_path='data/roots_mapped.json',
            word_to_root_path='data/word_to_root.json'):
    roots_mapped = load_roots_mapped(roots_mapped_path)
    word_to_root = load_word_to_root(word_to_root_path)
    return analyze_text(input_text, roots_mapped, word_to_root)


# ============================================================
# 8. اختبار سريع
# ============================================================

if __name__ == '__main__':
    print("جاري تحميل البيانات...")
    roots_mapped = load_roots_mapped()
    word_to_root = load_word_to_root()
    print(f"القاموس: {len(word_to_root)} كلمة\n")

    # اختبار جذر مباشر
    root_data = get_root_data('كتب', roots_mapped)
    if root_data:
        concept = extract_concept(root_data)
        print(summarize_concept(concept))
        print()

    # اختبار نص خارجي
    test_text = "الكتاب هو أساس العلم والمعرفة"
    result = analyze_text(test_text, roots_mapped, word_to_root)

    print(f"النص: {result['original_text']}")
    print(f"الكلمات المحللة: {result['matched_words']} / {result['total_words']}")
    print(f"لم تُعثر عليها: {result['not_found']}")
    print()

    for word, data in result['analyzed_words'].items():
        print(f"كلمة '{word}' ← جذر '{data['root']}'")
        print(summarize_concept(data['concept']))
        print()