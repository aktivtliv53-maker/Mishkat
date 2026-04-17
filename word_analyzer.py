import json
from final_finder_v2 import normalize, find_root, strip_affixes

# -----------------------------------------
# تحميل JSON
# -----------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

LETTER_TABLE = load_json("data/letter_master_table.json")
LETTER_INDEX = {entry["الحرف"]: entry for entry in LETTER_TABLE}

WORD_ROOT_MAP = load_json("data/word_to_root.json")
ROOTS_DATA = load_json("data/roots_mapped.json")
ROOTS_INDEX = {normalize(r["root"]): r for r in ROOTS_DATA}

# -----------------------------------------
# تحليل الحروف داخل الكلمة
# -----------------------------------------
def analyze_letters(word):
    word_norm = normalize(word)
    letters = list(word_norm)

    analysis = []

    for i, ch in enumerate(letters):
        entry = LETTER_INDEX.get(ch)

        analysis.append({
            "حرف": ch,
            "موقع": (
                "بداية" if i == 0 else
                "نهاية" if i == len(letters)-1 else
                "وسط"
            ),
            "عدد_الجذور": entry.get("عدد_الجذور") if entry else None,
            "القيمة_الوظيفية": entry.get("القيمة_الوظيفية") if entry else None,
            "المجال_الغالب": entry.get("المجال_الغالب") if entry else None,
        })

    return analysis

# -----------------------------------------
# تحليل الكلمة بالكامل
# -----------------------------------------
def analyze_word(word):
    word_norm = normalize(word)

    # 1) الجذر
    root = find_root(word, WORD_ROOT_MAP, ROOTS_INDEX)
    root_entry = ROOTS_INDEX.get(root) if root else None

    # 2) البادئات واللواحق
    stripped_candidates = strip_affixes(word_norm)
    stripped = max(stripped_candidates, key=len)

    # 3) تحليل الحروف
    letters_info = analyze_letters(word)

    # 4) بناء التقرير النهائي
    return {
        "الكلمة": word,
        "النظيفة": word_norm,
        "الجذر": root,
        "معنى_الجذر": root_entry.get("meanings") if root_entry else None,
        "الجذر_في_البيانات": root_entry,
        "الحروف": letters_info,
        "أقوى_صيغة_مجردة": stripped,
        "البادئات_واللواحق": list(stripped_candidates),
    }

# -----------------------------------------
# اختبار سريع
# -----------------------------------------
if __name__ == "__main__":
    import json as _json

    test_words = [
        "الكتاب","للمتقين","يؤمنون","الغيب",
        "الصلاة","الرحيم","رزقناهم","يعلمون",
        "ذلك","كتاب","رحم","صلاه","المتقين",
        "الملائكة","بالصالحات","صلاتهم","صلاتك"
    ]

    for w in test_words:
        print("\n==============================")
        result = analyze_word(w)
        print(_json.dumps(result, ensure_ascii=False, indent=2))