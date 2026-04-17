import json
from collections import defaultdict

with open("data/roots_mapped.json", encoding="utf-8") as f:
    data = json.load(f)

ayah_index = defaultdict(list)

for entry in data:
    root = entry["root"]
    for ayah in entry["ayahs"]:
        key = f"{ayah['surah_number']}:{ayah['ayah_number']}"
        ayah_index[key].append(root)

with open("data/ayah_roots_index.json", "w", encoding="utf-8") as f:
    json.dump(ayah_index, f, ensure_ascii=False, indent=2)

print(f"✅ تم بناء الفهرس — {len(ayah_index)} آية")