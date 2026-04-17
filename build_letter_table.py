import json
import os

data_dir = "data"
letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"

results = []

for letter in letters:
    filename = f"letter_stats_{letter}.json"
    filepath = os.path.join(data_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️ مفقود: {letter}")
        continue
    
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    
    top_roots = [r["root"] for r in data.get("top_roots", [])[:3]]
    
    results.append({
        "الحرف": letter,
        "عدد_الجذور": data.get("total_roots_containing", 0),
        "القيمة_الوظيفية": data.get("functional_value", 0),
        "المجال_الغالب": data.get("dominant_field", "—"),
        "بداية": f"{data.get('position_profile', {}).get('بداية', 0)*100:.1f}%",
        "وسط": f"{data.get('position_profile', {}).get('وسط', 0)*100:.1f}%",
        "نهاية": f"{data.get('position_profile', {}).get('نهاية', 0)*100:.1f}%",
        "أعلى_الجذور": "، ".join(top_roots)
    })

# طباعة الجدول
print(f"\n{'='*90}")
print(f"{'الحرف':<6} {'الجذور':<8} {'الوظيفية':<10} {'المجال':<10} {'بداية':<8} {'وسط':<8} {'نهاية':<8} {'أعلى الجذور'}")
print(f"{'='*90}")

for r in results:
    print(f"{r['الحرف']:<6} {r['عدد_الجذور']:<8} {r['القيمة_الوظيفية']:<10} {r['المجال_الغالب']:<10} {r['بداية']:<8} {r['وسط']:<8} {r['نهاية']:<8} {r['أعلى_الجذور']}")

# حفظ JSON
with open("data/letter_master_table.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✅ تم الحفظ في data/letter_master_table.json")
print(f"عدد الحروف: {len(results)}")