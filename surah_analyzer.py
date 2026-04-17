import json
from verse_analyzer import analyze_ayah
from final_finder_v2 import normalize

# -----------------------------------------
# تحميل JSON
# -----------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

QURAN_DATA = load_json("data/quran.json")

# -----------------------------------------
# جلب كل آيات السورة
# -----------------------------------------
def get_surah_ayahs(surah_number):
    return [a for a in QURAN_DATA if a.get("surah_number") == surah_number]

# -----------------------------------------
# تحليل سورة كاملة
# -----------------------------------------
def analyze_surah(surah_number):
    ayahs = get_surah_ayahs(surah_number)

    if not ayahs:
        return {
            "رقم_السورة": surah_number,
            "خطأ": "السورة غير موجودة في البيانات"
        }

    surah_name = ayahs[0].get("surah_name")

    all_ayahs_analysis = []
    roots_counter = {}
    letters_counter = {}

    for a in ayahs:
        ayah_number = a.get("ayah_number")
        analysis = analyze_ayah(surah_number, ayah_number)
        all_ayahs_analysis.append(analysis)

        # تجميع جذور السورة
        root_map = analysis["تحليل"]["تكرار_الجذور"]
        for r, c in root_map.items():
            roots_counter[r] = roots_counter.get(r, 0) + c

        # تجميع الحروف
        letter_map = analysis["تحليل"]["تكرار_الحروف"]
        for h, c in letter_map.items():
            letters_counter[h] = letters_counter.get(h, 0) + c

    # أقوى الجذور
    sorted_roots = sorted(roots_counter.items(), key=lambda x: x[1], reverse=True)

    # أقوى الحروف
    sorted_letters = sorted(letters_counter.items(), key=lambda x: x[1], reverse=True)

    return {
        "اسم_السورة": surah_name,
        "رقم_السورة": surah_number,
        "عدد_الآيات": len(ayahs),
        "تحليل_الآيات": all_ayahs_analysis,
        "تكرار_الجذور": roots_counter,
        "أقوى_الجذور": sorted_roots[:10],
        "تكرار_الحروف": letters_counter,
        "أقوى_الحروف": sorted_letters[:10],
    }

# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":
    import json as _json

    tests = [1, 2, 33, 36, 55, 112]

    for s in tests:
        print("\n==============================")
        result = analyze_surah(s)
        print(_json.dumps(result, ensure_ascii=False, indent=2))