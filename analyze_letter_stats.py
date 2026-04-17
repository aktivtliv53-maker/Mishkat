import json
import re
from collections import Counter

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def analyze_letter(letter, roots_data):
    letter = normalize(letter)
    
    position_start = 0
    position_mid = 0
    position_end = 0
    total_roots = 0
    
    cooccurrence = Counter()
    semantic_fields = Counter()
    pattern_roots = []

    for entry in roots_data:
        root = normalize(entry["root"])
        if letter not in root:
            continue

        total_roots += 1

        # موقع الحرف في الجذر
        if root.startswith(letter):
            position_start += 1
        if len(root) >= 2 and root[1] == letter:
            position_mid += 1
        if root.endswith(letter):
            position_end += 1

        # التكرار مع الجذور الأخرى
        for ayah in entry.get("ayahs", []):
            cooccurrence[entry["root"]] += 1

        # المجال الدلالي من المعنى
        meaning = entry.get("meanings", "")
        if any(w in meaning for w in ["حركة", "جريان", "سير", "انتقال", "حرك"]):
            semantic_fields["حركة"] += 1
        if any(w in meaning for w in ["سكون", "ثبات", "استقرار", "رسوخ"]):
            semantic_fields["سكون"] += 1
        if any(w in meaning for w in ["علو", "ارتفاع", "صعود", "سمو"]):
            semantic_fields["علوي"] += 1
        if any(w in meaning for w in ["نزول", "هبوط", "سفل"]):
            semantic_fields["سفلي"] += 1
        if any(w in meaning for w in ["مادة", "جسم", "أرض", "شيء"]):
            semantic_fields["مادي"] += 1
        if any(w in meaning for w in ["معنى", "روح", "نفس", "قلب", "إدراك"]):
            semantic_fields["معنوي"] += 1
        if any(w in meaning for w in ["احتواء", "وعاء", "جمع", "ضم"]):
            semantic_fields["احتواء"] += 1
        if any(w in meaning for w in ["انتشار", "توسع", "امتداد"]):
            semantic_fields["انتشار"] += 1

        pattern_roots.append(root)

    # حساب النسب
    total = max(total_roots, 1)
    position_profile = {
        "بداية": round(position_start / total, 3),
        "وسط": round(position_mid / total, 3),
        "نهاية": round(position_end / total, 3)
    }

    # أعلى جذور تكراراً
    top_roots = sorted(roots_data, key=lambda x: x["ayah_count"], reverse=True)
    top_with_letter = [
        {"root": r["root"], "ayah_count": r["ayah_count"], "meanings": r["meanings"]}
        for r in top_roots if letter in normalize(r["root"])
    ][:10]

    # القيمة الوظيفية
    dominant_field = semantic_fields.most_common(1)[0] if semantic_fields else ("غير محدد", 0)
    position_weight = (
        position_start * 1.0 +
        position_mid * 0.7 +
        position_end * 0.9
    ) / max(total_roots, 1)
    density = min(total_roots / 100, 1.0)
    functional_value = round((position_weight * 0.5 + density * 0.5), 4)

    return {
        "letter": letter,
        "total_roots_containing": total_roots,
        "position_profile": position_profile,
        "semantic_field_bias": dict(semantic_fields.most_common()),
        "dominant_field": dominant_field[0],
        "top_roots": top_with_letter,
        "functional_value": functional_value,
        "position_weight": round(position_weight, 4)
    }

def main():
    data = load_json("data/roots_mapped.json")
    letter = input("أدخل الحرف: ").strip()
    
    result = analyze_letter(letter, data)
    
    print(f"\n{'='*50}")
    print(f"الحرف: {result['letter']}")
    print(f"عدد الجذور التي يظهر فيها: {result['total_roots_containing']}")
    print(f"\nملف الموقع:")
    for pos, val in result['position_profile'].items():
        print(f"  {pos}: {val*100:.1f}%")
    print(f"\nالمجال الدلالي الغالب: {result['dominant_field']}")
    print(f"المجالات: {result['semantic_field_bias']}")
    print(f"\nالقيمة الوظيفية: {result['functional_value']}")
    print(f"\nأعلى الجذور:")
    for r in result['top_roots'][:5]:
        print(f"  {r['root']}: {r['ayah_count']} آية — {r['meanings']}")
    
    output = f"data/letter_stats_{letter}.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ تم الحفظ في {output}")

main()