import json
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SURAH_TYPE = {
    1: "مكية", 2: "مدنية", 3: "مدنية", 4: "مدنية", 5: "مدنية",
    6: "مكية", 7: "مكية", 8: "مدنية", 9: "مدنية", 10: "مكية",
    11: "مكية", 12: "مكية", 13: "مدنية", 14: "مكية", 15: "مكية",
    16: "مكية", 17: "مكية", 18: "مكية", 19: "مكية", 20: "مكية",
    21: "مكية", 22: "مدنية", 23: "مكية", 24: "مدنية", 25: "مكية",
    26: "مكية", 27: "مكية", 28: "مكية", 29: "مكية", 30: "مكية",
    31: "مكية", 32: "مكية", 33: "مدنية", 34: "مكية", 35: "مكية",
    36: "مكية", 37: "مكية", 38: "مكية", 39: "مكية", 40: "مكية",
    41: "مكية", 42: "مكية", 43: "مكية", 44: "مكية", 45: "مكية",
    46: "مكية", 47: "مدنية", 48: "مدنية", 49: "مدنية", 50: "مكية",
    51: "مكية", 52: "مكية", 53: "مكية", 54: "مكية", 55: "مكية",
    56: "مكية", 57: "مدنية", 58: "مدنية", 59: "مدنية", 60: "مدنية",
    61: "مدنية", 62: "مدنية", 63: "مدنية", 64: "مدنية", 65: "مدنية",
    66: "مدنية", 67: "مكية", 68: "مكية", 69: "مكية", 70: "مكية",
    71: "مكية", 72: "مكية", 73: "مكية", 74: "مكية", 75: "مكية",
    76: "مكية", 77: "مكية", 78: "مكية", 79: "مكية", 80: "مكية",
    81: "مكية", 82: "مكية", 83: "مكية", 84: "مكية", 85: "مكية",
    86: "مكية", 87: "مكية", 88: "مكية", 89: "مكية", 90: "مكية",
    91: "مكية", 92: "مكية", 93: "مكية", 94: "مكية", 95: "مكية",
    96: "مكية", 97: "مكية", 98: "مدنية", 99: "مدنية", 100: "مكية",
    101: "مكية", 102: "مكية", 103: "مكية", 104: "مكية", 105: "مكية",
    106: "مكية", 107: "مكية", 108: "مكية", 109: "مكية", 110: "مدنية",
    111: "مكية", 112: "مكية", 113: "مكية", 114: "مكية"
}

def load_roots_mapped():
    path = os.path.join(BASE_DIR, "data", "roots_mapped.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def get_root_concept(root_entry):
    ayahs = root_entry.get("ayahs", [])
    if not ayahs:
        return {
            "root": root_entry["root"],
            "meanings": root_entry["meanings"],
            "ayah_count": 0,
            "contexts": [],
            "concept": "لا يوجد توظيف قرآني مرصود"
        }

    contexts = []
    for ayah in ayahs:
        surah_type = SURAH_TYPE.get(ayah["surah_number"], "غير محدد")
        contexts.append({
            "surah": ayah["surah"],
            "surah_number": ayah["surah_number"],
            "ayah_number": ayah["ayah_number"],
            "text": ayah["text"],
            "context_type": surah_type
        })

    context_types = [c["context_type"] for c in contexts]
    count = Counter(context_types)
    makki = count.get("مكية", 0)
    madani = count.get("مدنية", 0)

    if makki > madani:
        dominant = "مكية — عقيدة وتأسيس"
    elif madani > makki:
        dominant = "مدنية — تشريع وبناء مجتمع"
    else:
        dominant = "متوازن — مكي ومدني"

    concept = f'الجذر "{root_entry["root"]}" بمعنى ({root_entry["meanings"]}) '
    concept += f'يظهر في {len(ayahs)} آية — '
    concept += f'{makki} مكية و{madani} مدنية. '
    concept += f'طابعه الغالب: {dominant}'

    return {
        "root": root_entry["root"],
        "meanings": root_entry["meanings"],
        "ayah_count": len(ayahs),
        "makki_count": makki,
        "madani_count": madani,
        "dominant": dominant,
        "contexts": contexts,
        "concept": concept
    }

def search_root(query, roots_mapped):
    for entry in roots_mapped:
        if entry["root"] == query:
            return get_root_concept(entry)
    return None

if __name__ == "__main__":
    data = load_roots_mapped()

    test_root = "رحم"
    result = search_root(test_root, data)

    if result:
        print(f"الجذر: {result['root']}")
        print(f"المعنى: {result['meanings']}")
        print(f"عدد الآيات: {result['ayah_count']}")
        print(f"مكية: {result['makki_count']} | مدنية: {result['madani_count']}")
        print(f"الطابع الغالب: {result['dominant']}")
        print(f"\nالمفهوم: {result['concept']}")
        print("\nأول 3 آيات:")
        for c in result['contexts'][:3]:
            print(f"  [{c['surah']} {c['ayah_number']} — {c['context_type']}]: {c['text'][:60]}...")
    else:
        print("الجذر غير موجود")