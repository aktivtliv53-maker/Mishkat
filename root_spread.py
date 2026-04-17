import json
from final_finder_v2 import normalize

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

def compute_root_spread(root_entry):
    if not root_entry:
        return 0, set()

    ayahs = root_entry.get("ayahs", [])
    surahs = set()

    for a in ayahs:
        sn = a.get("surah_number")
        if sn is not None:
            surahs.add(sn)

    return len(surahs), surahs

def get_root_spread(root):
    entry = get_root_entry(root)
    return compute_root_spread(entry)