import json
import re
from itertools import combinations

# -----------------------------------------
# تحميل JSON
# -----------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# -----------------------------------------
# التطبيع (Normalization)
# -----------------------------------------
def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)

    # الهمزات
    text = text.replace("أ","ا").replace("إ","ا").replace("آ","ا")
    text = text.replace("ؤ","و")
    text = text.replace("ئ","ي")

    # التاء المربوطة → ت
    text = text.replace("ة","ت")

    # الألف المقصورة → ي
    text = text.replace("ى","ي")

    return text.strip()

# -----------------------------------------
# البادئات واللواحق
# -----------------------------------------
PREFIXES = ["وال","فال","بال","كال","لل","ال","و","ف","ب","ل","س","ك"]
SUFFIXES = [
    "تموهم","تموها","ناهم","ناها","تموا","كموه",
    "هما","هم","كم","هن","نا","ها","وا","ون","ين","ان","ات",
    "تم","تن","وه","يه","ته","ني","ه","ك","ي","ن","ا"
]

# -----------------------------------------
# إزالة البادئات واللواحق
# -----------------------------------------
def strip_affixes(word):
    candidates = {word}

    # 1) إزالة اللواحق
    for s in sorted(SUFFIXES, key=len, reverse=True):
        if word.endswith(s) and len(word) > len(s) + 1:
            candidates.add(word[:-len(s)])

    # 2) إزالة البادئات
    for p in sorted(PREFIXES, key=len, reverse=True):
        if word.startswith(p) and len(word) > len(p) + 1:
            stripped = word[len(p):]
            candidates.add(stripped)

            # 3) إزالة لواحق بعد البادئة
            for s in sorted(SUFFIXES, key=len, reverse=True):
                if stripped.endswith(s) and len(stripped) > len(s) + 1:
                    candidates.add(stripped[:-len(s)])

    return candidates

# -----------------------------------------
# توليد جذور ثلاثية محتملة
# -----------------------------------------
def generate_triliteral_candidates(word):
    word = normalize(word)
    letters = list(word)
    candidates = set()

    # كل التركيبات الثلاثية الممكنة
    for combo in combinations(letters, 3):
        candidates.add("".join(combo))

    # إضافة النسخ المرتبة
    for c in list(candidates):
        candidates.add("".join(sorted(c)))

    return candidates

# -----------------------------------------
# إيجاد الجذر
# -----------------------------------------
def find_root(word, word_root_map, roots_index):
    word_clean = normalize(word)

    # 1) بحث مباشر
    if word_clean in word_root_map:
        return word_root_map[word_clean]

    # 2) بعد إزالة البادئات واللواحق
    candidates = strip_affixes(word_clean)
    for candidate in sorted(candidates, key=len, reverse=True):
        if candidate in word_root_map:
            return word_root_map[candidate]

    # 3) توليد جذور ثلاثية
    tri_candidates = generate_triliteral_candidates(word_clean)
    for tri in tri_candidates:
        if tri in roots_index:
            return tri

    return None