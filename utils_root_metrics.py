import json
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOTS_PATH = os.path.join(BASE_DIR, "data", "roots_mapped.json")

def load_roots():
    with open(ROOTS_PATH, encoding="utf-8") as f:
        return json.load(f)

ROOTS_DATA = load_roots()

def get_root_entry(root):
    for entry in ROOTS_DATA:
        if entry.get("root") == root:
            return entry
    return None

def compute_root_metrics(entry):
    ayahs = entry.get("ayahs", [])
    strength = len(ayahs)
    surahs = set()
    all_words = []
    ayah_lengths = []

    for a in ayahs:
        surahs.add(a.get("surah_number"))
        words = a.get("text", "").split()
        all_words.extend(words)
        ayah_lengths.append(len(words))

    spread = len(surahs)
    unique_words = set(all_words)
    total_words = len(all_words)

    diversity = len(unique_words) / total_words if total_words else 0
    avg_ayah_len = sum(ayah_lengths) / len(ayah_lengths) if ayah_lengths else 0
    context_density = len(unique_words) / (strength + 1e-6)

    concept_weight = (
        0.35 * np.tanh(strength / 80) +
        0.25 * np.tanh(spread / 20) +
        0.25 * min(1, diversity * 4) +
        0.15 * min(1, context_density / 10)
    )

    return {
        "strength": strength,
        "spread": spread,
        "diversity": diversity,
        "avg_ayah_len": avg_ayah_len,
        "context_density": context_density,
        "concept_weight": concept_weight,
    }