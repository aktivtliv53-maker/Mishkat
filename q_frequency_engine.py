# q_frequency_engine.py
# Q-Frequency Engine — تحليل ترددي للآية بناءً على مدارات الأحرف السبعة

from collections import Counter, defaultdict

# تعريف مدارات الأحرف السبعة
LETTER_BANDS = {
    "القوة": set("قصطدكحكم"),      # يمكنك تعديل/تنقية المجموعات لاحقاً
    "المادة": set("لمنب"),
    "الهوية": set("هوي"),
    "السر": set("عغظ"),
    "البيان": set("سشففز"),
    "الرحم": set("حجخ"),
    "الوعي": set("زردذ"),
}

# حروف تُهمل في الحساب (تنوين، حركات، إلخ)
IGNORED_CHARS = set("ًٌٍَُِّْـ،؛؟.!\"'«»()[]{} ")

def normalize_text(text: str) -> str:
    """تنظيف مبدئي للنص (يمكن تطويره لاحقاً)."""
    return "".join(ch for ch in text if ch not in IGNORED_CHARS)

def classify_letter(ch: str) -> str | None:
    """إرجاع اسم المدار الذي ينتمي له الحرف، أو None إن لم يُصنَّف."""
    for band_name, letters in LETTER_BANDS.items():
        if ch in letters:
            return band_name
    return None

def analyze_verse(verse: str) -> dict:
    """
    يُرجع:
      - counts_per_band: عدد الحروف في كل مدار
      - counts_per_letter: عدد كل حرف
      - total_letters: مجموع الحروف المصنَّفة
    """
    verse_norm = normalize_text(verse)
    band_counts = Counter()
    letter_counts = Counter()

    for ch in verse_norm:
        band = classify_letter(ch)
        if band is not None:
            band_counts[band] += 1
            letter_counts[ch] += 1

    total_letters = sum(band_counts.values())

    # تحويل إلى شكل JSON‑ready
    return {
        "verse": verse,
        "total_letters": total_letters,
        "counts_per_band": dict(band_counts),
        "counts_per_letter": dict(letter_counts),
    }

if __name__ == "__main__":
    # اختبار سريع على آية التدبير
    verse = "يُدَبِّرُ الْأَمْرَ مِنَ السَّمَاءِ إِلَى الْأَرْضِ ثُمَّ يَعْرُجُ إِلَيْهِ فِي يَوْمٍ كَانَ مِقْدَارُهُ أَلْفَ سَنَةٍ مِمَّا تَعُدُّونَ"
    result = analyze_verse(verse)
    print("الآية:", result["verse"])
    print("مجموع الحروف المصنَّفة:", result["total_letters"])
    print("توزيع المدارات:", result["counts_per_band"])
    print("توزيع الحروف:", result["counts_per_letter"])