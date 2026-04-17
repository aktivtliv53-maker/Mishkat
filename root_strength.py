import json
from final_finder_v2 import normalize

# نفترض أن ملف الجذور موجود في:
# data/roots_index.json
# وفيه لكل جذر: { "root": "...", "ayahs": [ {..}, ... ] }

def load_roots(path="data/roots_index.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

ROOTS_DATA = load_roots()

def get_root_entry(root):
    root_norm = normalize(root)
    for entry in ROOTS_DATA:
        if normalize(entry.get("root", "")) == root_norm:
            return entry
    return None

def compute_root_strength(root_entry):
    if not root_entry:
        return 0
    ayahs = root_entry.get("ayahs", [])
    return len(ayahs)

def get_root_strength(root):
    entry = get_root_entry(root)
    return compute_root_strength(entry)