# ============================
#   Mishkat Data Loader v3.0
#   (Auto Path Detection)
# ============================

import os
import csv
import json


def load_quran(filename="quran.csv"):
    """
    يقوم بالبحث تلقائيًا عن ملف القرآن في عدة مسارات محتملة
    ويعيد أول ملف يجده بدون أي خطأ.
    """

    # المسارات المحتملة
    possible_paths = [
        filename,
        f"./{filename}",
        f"data/{filename}",
        f"./data/{filename}",
        f"../data/{filename}",
        os.path.join(os.path.dirname(__file__), "..", "data", filename),
        os.path.join(os.path.dirname(__file__), "..", "..", "data", filename),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return _load_quran_file(path)

    raise FileNotFoundError(
        f"❌ لم يتم العثور على ملف القرآن في أي من المسارات التالية:\n{possible_paths}"
    )


def _load_quran_file(path):
    """
    تحميل ملف القرآن سواء كان CSV أو JSON
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        return _load_csv(path)

    elif ext == ".json":
        return _load_json(path)

    else:
        raise ValueError(f"صيغة غير مدعومة: {ext}")


def _load_csv(path):
    quran = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            quran.append({
                "surah_number": int(row.get("surah_number") or row.get("surah") or 0),
                "ayah_number": int(row.get("ayah_number") or row.get("ayah") or 0),
                "text": row.get("text", "")
            })
    return quran


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    quran = []
    for ay in data:
        quran.append({
            "surah_number": int(ay.get("surah_number") or ay.get("surah") or 0),
            "ayah_number": int(ay.get("ayah_number") or ay.get("ayah") or 0),
            "text": ay.get("text", "")
        })
    return quran
