import json
import re
from collections import Counter
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ى", "ي")
    return text.strip()

def extract_ta_words(quran_data):
    """يستخرج كل الكلمات المنتهية بتاء مربوطة أو مفتوحة"""
    ta_words = []
    
    for ayah in quran_data:
        text = ayah["text"]
        words = text.split()
        for word in words:
            clean = normalize(word)
            # كلمات تنتهي بـ ة أو ت
            original = re.sub(r"[ًٌٍَُِّْـٰ]", "", word)
            if original.endswith("ة") or original.endswith("ت"):
                ta_words.append({
                    "word": original,
                    "clean": clean,
                    "ayah_index": ayah["index"],
                    "surah": ayah["surah_name"],
                    "ayah_number": ayah["ayah_number"],
                    "text": text
                })
    
    return ta_words

def group_by_root(ta_words, roots_data):
    """يجمع الكلمات مع جذورها"""
    root_index = {normalize(r["root"]): r for r in roots_data}
    
    grouped = {}
    for word_data in ta_words:
        clean = word_data["clean"]
        # ابحث عن الجذر
        for root, root_entry in root_index.items():
            if root in clean and len(root) >= 2:
                if root not in grouped:
                    grouped[root] = {
                        "root": root_entry["root"],
                        "meanings": root_entry.get("meanings", ""),
                        "with_ta": [],
                        "without_ta": []
                    }
                grouped[root]["with_ta"].append(word_data)
                break
    
    return grouped

def analyze_ta_pattern(grouped, sample_size=15):
    """يحلل نمط التاء مع مجموعة من الجذور"""
    
    samples = []
    count = 0
    for root, data in grouped.items():
        if count >= sample_size:
            break
        if len(data["with_ta"]) >= 2:
            samples.append({
                "root": data["root"],
                "meanings": data["meanings"],
                "examples": [w["word"] for w in data["with_ta"][:5]]
            })
            count += 1
    
    samples_text = "\n".join([
        f"- جذر {s['root']} ({s['meanings']}): {', '.join(s['examples'])}"
        for s in samples
    ])
    
    prompt = f"""أنت باحث في اللغة القرآنية.

هذه كلمات قرآنية تنتهي بالتاء (ة أو ت) مع جذورها:
{samples_text}

الفرضية المطروحة: التاء في القرآن ليست علامة تأنيث بل علامة "وحدة مكتملة" أو "حالة محددة".

من خلال هذه الأمثلة:
1. هل تدعم هذه الكلمات الفرضية أم تعارضها؟
2. ما النمط الذي تلاحظه فعلاً؟
3. اذكر مثالاً يدعم الفرضية ومثالاً يعارضها.

أجب بدقة وموضوعية في 4 جمل فقط."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def main():
    print("جاري تحميل البيانات...")
    quran_data = load_json("data/matrix_data.json")
    roots_data = load_json("data/roots_mapped.json")
    
    print("جاري استخراج كلمات التاء...")
    ta_words = extract_ta_words(quran_data)
    print(f"عدد الكلمات المنتهية بتاء: {len(ta_words)}")
    
    print("جاري تجميع الكلمات مع جذورها...")
    grouped = group_by_root(ta_words, roots_data)
    print(f"عدد الجذور المرتبطة: {len(grouped)}")
    
    print("\nجاري التحليل...")
    analysis = analyze_ta_pattern(grouped)
    
    print(f"\n{'='*50}")
    print("نتيجة اختبار نظرية التاء:")
    print(f"{'='*50}")
    print(analysis)
    
    result = {
        "total_ta_words": len(ta_words),
        "total_roots": len(grouped),
        "analysis": analysis,
        "sample_words": list(grouped.keys())[:20]
    }
    
    with open("data/ta_theory_test.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم الحفظ في data/ta_theory_test.json")

main()