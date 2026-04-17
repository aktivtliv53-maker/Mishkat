import json
from word_analyzer import analyze_word
from final_finder_v2 import normalize

# -----------------------------------------
# تحميل JSON
# -----------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ملف القرآن بصيغة:
# [
#   {"index":1, "surah_number":1, "ayah_number":1, "surah_name":"الفاتحة", "text":"..."},
#   ...
# ]
QURAN_DATA = load_json("data/quran.json")

# -----------------------------------------
# تحليل آية نصيًا
# -----------------------------------------
def analyze_ayah_text(text):
    raw_words = text.split()
    words = [w.strip("،؛.؟!ۚۖۗۛۙۜ۝") for w in raw_words if w.strip()]

    word_analyses = []
    roots_counter = {}
    letters_counter = {}

    for w in words:
        wa = analyze_word(w)
        word_analyses.append(wa)

        # عدّ الجذور
        root = wa.get("الجذر")
        if root:
            roots_counter[root] = roots_counter.get(root, 0) + 1

        # عدّ الحروف
        for h in wa.get("الحروف", []):
            ch = h.get("حرف")
            if ch:
                letters_counter[ch] = letters_counter.get(ch, 0) + 1

    return {
        "النص": text,
        "عدد_الكلمات": len(words),
        "تحليل_الكلمات": word_analyses,
        "تكرار_الجذور": roots_counter,
        "تكرار_الحروف": letters_counter,
    }

# -----------------------------------------
# إيجاد آية من ملف القرآن
# -----------------------------------------
def find_ayah(surah_number, ayah_number):
    for a in QURAN_DATA:
        if a.get("surah_number") == surah_number and a.get("ayah_number") == ayah_number:
            return a
    return None

# -----------------------------------------
# تحليل آية كاملة
# -----------------------------------------
def analyze_ayah(surah_number, ayah_number):
    ayah = find_ayah(surah_number, ayah_number)
    if not ayah:
        return {
            "سورة": surah_number,
            "آية": ayah_number,
            "خطأ": "الآية غير موجودة في البيانات"
        }

    text = ayah.get("text", "")
    analysis = analyze_ayah_text(text)

    return {
        "سورة": ayah.get("surah_name"),
        "رقم_السورة": surah_number,
        "رقم_الآية": ayah_number,
        "النص": text,
        "تحليل": analysis,
    }

# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":
    import json as _json

    tests = [
        (1, 1),
        (1, 2),
        (2, 3),
        (33, 56),
        (70, 23),
        (108, 2),
    ]

    for s, a in tests:
        print("\n==============================")
        result = analyze_ayah(s, a)
        print(_json.dumps(result, ensure_ascii=False, indent=2))