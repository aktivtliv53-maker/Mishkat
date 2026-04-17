import json
import re
import time
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

def extract_unique_ta_words(quran_data):
    """يستخرج الكلمات الفريدة المنتهية بتاء"""
    seen = set()
    ta_words = []
    
    for ayah in quran_data:
        words = ayah["text"].split()
        for word in words:
            original = re.sub(r"[ًٌٍَُِّْـٰ]", "", word)
            if (original.endswith("ة") or original.endswith("ت")) and original not in seen:
                seen.add(original)
                ta_words.append({
                    "word": original,
                    "surah": ayah["surah_name"],
                    "ayah_number": ayah["ayah_number"],
                    "text": ayah["text"]
                })
    
    return ta_words

def classify_batch(batch):
    """يصنف مجموعة من الكلمات"""
    words_text = "\n".join([
        f"- {w['word']} (في {w['surah']} {w['ayah_number']}): {w['text'][:60]}"
        for w in batch
    ])
    
    prompt = f"""أنت باحث في اللغة القرآنية.

هذه كلمات قرآنية تنتهي بالتاء:
{words_text}

لكل كلمة، حدد دور التاء فيها من هذه الأنواع فقط:
1. وحدة_مكتملة — التاء تغلق الكيان وتحدده (صلاة، رحمة، قرية)
2. حالة_محددة — التاء تصف حالة أو طور (مؤمنات، مسلمات)
3. فعل_مكتمل — التاء تختم الفعل (كتبت، ثمرت)
4. جمع_مفتوح — التاء تفتح العدد (آيات، سماوات)
5. غير_محدد — لا ينطبق عليها أي نوع

أجب بصيغة JSON فقط هكذا بدون أي نص إضافي:
{{"results": [{{"word": "الكلمة", "type": "النوع", "reason": "سبب قصير"}}]}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"خطأ: {e}")
        return {"results": []}

def main():
    print("جاري تحميل البيانات...")
    quran_data = load_json("data/matrix_data.json")
    
    print("جاري استخراج الكلمات الفريدة...")
    ta_words = extract_unique_ta_words(quran_data)
    print(f"عدد الكلمات الفريدة: {len(ta_words)}")
    
    # تصنيف على دفعات
    batch_size = 10
    all_results = []
    counts = {
        "وحدة_مكتملة": 0,
        "حالة_محددة": 0,
        "فعل_مكتمل": 0,
        "جمع_مفتوح": 0,
        "غير_محدد": 0
    }
    
    total_batches = len(ta_words) // batch_size + 1
    
    for i in range(0, min(len(ta_words), 200), batch_size):
        batch = ta_words[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"جاري تصنيف الدفعة {batch_num}/{min(total_batches, 20)}...")
        
        result = classify_batch(batch)
        
        for r in result.get("results", []):
            all_results.append(r)
            t = r.get("type", "غير_محدد")
            if t in counts:
                counts[t] += 1
            else:
                counts["غير_محدد"] += 1
        
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print("نتائج التصنيف:")
    print(f"{'='*50}")
    total = sum(counts.values())
    for category, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        pct = count/total*100 if total > 0 else 0
        print(f"{category}: {count} ({pct:.1f}%)")
    
    output = {
        "total_classified": len(all_results),
        "counts": counts,
        "results": all_results
    }
    
    with open("data/ta_classification.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم الحفظ في data/ta_classification.json")

main()