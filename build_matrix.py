import json

# تحميل ملف الجذور
with open("data/roots_mapped.json", "r", encoding="utf-8") as f:
    roots = json.load(f)

matrix = {}

for entry in roots:
    root = entry["root"]
    for ayah in entry["ayahs"]:
        surah = str(ayah["surah_number"])
        key = f"{surah}:{root}"
        matrix[key] = matrix.get(key, 0) + 1

with open("data/matrix_data.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, ensure_ascii=False, indent=2)

print("matrix_data.json جاهز 100%")