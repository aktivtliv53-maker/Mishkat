# root_radar.py
# Root Radar 2.0 — رادار الجذور السباعي

import json
import matplotlib.pyplot as plt
import numpy as np

# المدارات السبعة
BANDS = [
    "القوة",
    "المادة",
    "الهوية",
    "السر",
    "البيان",
    "الرحم",
    "الوعي"
]

# خريطة الحروف إلى المدارات
LETTER_BANDS = {
    "القوة": set("قصطدك"),
    "المادة": set("لمنب"),
    "الهوية": set("هوي"),
    "السر": set("عغظ"),
    "البيان": set("سشف"),
    "الرحم": set("حجخ"),
    "الوعي": set("زردذ"),
}

def classify_letter(ch):
    for band, letters in LETTER_BANDS.items():
        if ch in letters:
            return band
    return None

def analyze_root(root):
    band_counts = {b: 0 for b in BANDS}
    for ch in root:
        band = classify_letter(ch)
        if band:
            band_counts[band] += 1
    return band_counts

def plot_root_radar(root):
    data = analyze_root(root)
    values = list(data.values())
    values += values[:1]  # إغلاق الدائرة

    angles = np.linspace(0, 2 * np.pi, len(BANDS) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(BANDS, fontweight='bold')

    ax.set_title(f"رادار الجذر: {root}", fontsize=16, fontweight='bold')
    plt.show()

if __name__ == "__main__":
    plot_root_radar("شهد")