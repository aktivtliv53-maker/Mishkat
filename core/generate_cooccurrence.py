import json
from collections import defaultdict, Counter
from itertools import combinations

with open("data/ayah_roots_index.json", encoding="utf-8") as f:
    ayah_index = json.load(f)

root_freq = Counter()
root_ayahs = defaultdict(set)
co_counts = Counter()

for ayah_id, roots in ayah_index.items():
    unique_roots = set(roots)
    for r in unique_roots:
        root_freq[r] += 1
        root_ayahs[r].add(ayah_id)
    for a, b in combinations(sorted(unique_roots), 2):
        co_counts[tuple(sorted((a, b)))] += 1

network = defaultdict(lambda: {"freq": 0, "links": []})

for r, f in root_freq.items():
    network[r]["freq"] = f

for (a, b), inter in co_counts.items():
    union = len(root_ayahs[a] | root_ayahs[b])
    jaccard = inter / union if union > 0 else 0
    if jaccard >= 0.01 and inter >= 2:
        network[a]["links"].append({"target": b, "weight": round(jaccard, 4), "intersection": inter})
        network[b]["links"].append({"target": a, "weight": round(jaccard, 4), "intersection": inter})

with open("data/root_cooccurrence.json", "w", encoding="utf-8") as f:
    json.dump(network, f, ensure_ascii=False, indent=2)

print(f"✅ تم بناء شبكة التلازم — {len(network)} جذر")