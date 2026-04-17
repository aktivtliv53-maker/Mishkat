import json
from surah_analyzer import analyze_surah
from final_finder_v2 import normalize

# -----------------------------------------
# تحميل JSON
# -----------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

QURAN_DATA = load_json("data/quran.json")

# -----------------------------------------
# استخراج أرقام السور الموجودة في الملف
# -----------------------------------------
def get_all_surah_numbers():
    nums = set()
    for a in QURAN_DATA:
        n = a.get("surah_number")
        if n is not None:
            nums.add(n)
    return sorted(nums)

# -----------------------------------------
# تحليل القرآن كاملاً
# -----------------------------------------
def analyze_quran():
    surah_numbers = get_all_surah_numbers()

    all_surahs = []
    global_roots = {}
    global_letters = {}

    for sn in surah_numbers:
        s_analysis = analyze_surah(sn)
        all_surahs.append(s_analysis)

        # جذور السورة
        roots_map = s_analysis.get("تكرار_الجذور", {})
        for r, c in roots_map.items():
            global_roots[r] = global_roots.get(r, 0) + c

        # حروف السورة
        letters_map = s_analysis.get("تكرار_الحروف", {})
        for h, c in letters_map.items():
            global_letters[h] = global_letters.get(h, 0) + c

    # أقوى الجذور في القرآن
    sorted_roots = sorted(global_roots.items(), key=lambda x: x[1], reverse=True)

    # أقوى الحروف في القرآن
    sorted_letters = sorted(global_letters.items(), key=lambda x: x[1], reverse=True)

    return {
        "عدد_السور": len(surah_numbers),
        "تحليل_السور": all_surahs,
        "تكرار_الجذور_في_القرآن": global_roots,
        "أقوى_الجذور_في_القرآن": sorted_roots[:50],
        "تكرار_الحروف_في_القرآن": global_letters,
        "أقوى_الحروف_في_القرآن": sorted_letters[:50],
    }

# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":
    import json as _json

    result = analyze_quran()
    print(_json.dumps(result, ensure_ascii=False, indent=2))