# utils/data_loader.py — v11
# محرك تحميل القرآن — نسخة مستقرة وموسّعة

import pandas as pd

def load_quran(path: str = "data/quran.csv"):
    """
    تحميل القرآن من ملف CSV بصيغة:
    surah_number, ayah_number, text
    مع تجاهل أي أسطر تبدأ بـ # أو أسطر فارغة.
    """

    cleaned_rows = []

    # قراءة الملف الخام
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # تجاهل الأسطر الفارغة
            if not line:
                continue

            # تجاهل التعليقات
            if line.startswith("#"):
                continue

            cleaned_rows.append(line)

    # دمج الأسطر النظيفة
    from io import StringIO
    csv_data = "\n".join(cleaned_rows)

    # قراءة CSV
    df = pd.read_csv(StringIO(csv_data))

    quran = []
    for _, row in df.iterrows():
        try:
            surah = int(row["surah_number"])
            ayah = int(row["ayah_number"])
            text = str(row["text"])
        except:
            # تجاهل أي صف غير صالح
            continue

        quran.append({
            "surah_number": surah,
            "ayah_number": ayah,
            "text": text
        })

    return quran