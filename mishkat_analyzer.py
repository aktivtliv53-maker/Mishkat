import json
import re
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def find_root(word, roots_index):
    word_clean = normalize(word)
    prefixes = ["ال", "و", "ف", "ب", "ل", "س", "ك"]
    candidates = [word_clean]
    for p in prefixes:
        if word_clean.startswith(p) and len(word_clean) > len(p) + 1:
            candidates.append(word_clean[len(p):])
    
    for candidate in candidates:
        if candidate in roots_index:
            return roots_index[candidate]
        for root_clean, root_entry in roots_index.items():
            if len(root_clean) >= 2 and root_clean in candidate:
                return root_entry
    return None

def get_letter_data(letter, letter_table):
    letter_clean = normalize(letter)
    for entry in letter_table:
        if normalize(entry["الحرف"]) == letter_clean:
            return entry
    return None

def analyze_root_letters(root, letter_table):
    """يحلل الحروف المكونة للجذر"""
    root_clean = normalize(root)
    letters_analysis = []
    
    for i, letter in enumerate(root_clean):
        position = ["أول", "ثاني", "ثالث"][i] if i < 3 else "رابع"
        letter_data = get_letter_data(letter, letter_table)
        if letter_data:
            letters_analysis.append({
                "حرف": letter,
                "موقع": position,
                "مجال": letter_data.get("المجال_الغالب", ""),
                "وظيفية": letter_data.get("القيمة_الوظيفية", 0),
                "دور_بداية": letter_data.get("دور_صرفي_بداية", ""),
                "دور_نهاية": letter_data.get("دور_صرفي_نهاية", "")
            })
    
    return letters_analysis

def analyze_word(word, roots_index, roots_data, letter_table):
    """يحلل كلمة واحدة كاملاً"""
    root_entry = find_root(word, roots_index)
    if not root_entry:
        return None
    
    root = root_entry["root"]
    letters = analyze_root_letters(root, letter_table)
    ayahs = root_entry.get("ayahs", [])[:5]
    
    return {
        "كلمة": word,
        "جذر": root,
        "معاني_الجذر": root_entry.get("meanings", ""),
        "عدد_آيات": root_entry.get("ayah_count", 0),
        "تحليل_الحروف": letters,
        "نماذج_آيات": [a["text"][:80] for a in ayahs[:3]]
    }

def generate_insight(text, words_analysis):
    """يستخلص فهماً قرآنياً للنص كاملاً"""
    
    analysis_text = ""
    for w in words_analysis:
        if w:
            letters_summary = " + ".join([
                f"{l['حرف']}({l['مجال']})" 
                for l in w["تحليل_الحروف"]
            ])
            analysis_text += f"\n- {w['كلمة']} ← جذر {w['جذر']} ({w['معاني_الجذر']}) | حروف: {letters_summary}"
            if w["نماذج_آيات"]:
                analysis_text += f"\n  مثال قرآني: {w['نماذج_آيات'][0]}"

    prompt = f"""أنت باحث في اللغة القرآنية.

النص المدخل: {text}

تحليل الجذور والحروف:
{analysis_text}

بناءً على هذا التحليل القرآني للجذور والحروف:
1. ما المعنى العميق الذي يحمله هذا النص من منظور قرآني؟
2. ما العلاقة بين الجذور في هذا النص؟
3. ما الرسالة الجوهرية للنص؟

أجب في 3 فقرات موجزة."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def analyze_text(text, roots_index, roots_data, letter_table):
    """يحلل نصاً كاملاً"""
    words = text.split()
    words_analysis = []
    
    for word in words:
        if len(normalize(word)) >= 2:
            analysis = analyze_word(word, roots_index, roots_data, letter_table)
            if analysis:
                words_analysis.append(analysis)
    
    return words_analysis

def main():
    print("جاري تحميل البيانات...")
    roots_data = load_json("data/roots_mapped.json")
    letter_table = load_json("data/final_letter_table.json")["letter_table"]
    
    # بناء فهرس الجذور
    roots_index = {}
    for entry in roots_data:
        roots_index[normalize(entry["root"])] = entry
    
    print("✅ البيانات جاهزة\n")
    
    while True:
        print("="*60)
        print("1) تحليل نص عربي")
        print("2) تحليل آية قرآنية")
        print("3) خروج")
        choice = input("\nاختر: ").strip()
        
        if choice == "3":
            break
        
        if choice in ["1", "2"]:
            if choice == "1":
                text = input("أدخل النص: ").strip()
            else:
                surah = input("رقم السورة: ").strip()
                ayah = input("رقم الآية: ").strip()
                quran = load_json("data/matrix_data.json")
                found = [a for a in quran if str(a["surah_number"]) == surah and str(a["ayah_number"]) == ayah]
                if not found:
                    print("الآية غير موجودة")
                    continue
                text = found[0]["text"]
                print(f"\nالآية: {text}\n")
            
            print("\nجاري التحليل...")
            words_analysis = analyze_text(text, roots_index, roots_data, letter_table)
            
            print(f"\n{'='*60}")
            print("تحليل الكلمات:")
            print(f"{'='*60}")
            
            for w in words_analysis:
                print(f"\n● {w['كلمة']} ← جذر [{w['جذر']}] — {w['معاني_الجذر']} ({w['عدد_آيات']} آية)")
                for l in w["تحليل_الحروف"]:
                    print(f"  {l['موقع']}: {l['حرف']} | مجال: {l['مجال']} | وظيفية: {l['وظيفية']}")
            
            print(f"\n{'='*60}")
            print("الفهم القرآني للنص:")
            print(f"{'='*60}")
            insight = generate_insight(text, words_analysis)
            print(insight)
            
            # حفظ النتيجة
            output = {
                "نص": text,
                "تحليل_الكلمات": words_analysis,
                "فهم_قرآني": insight
            }
            with open("data/last_analysis.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print("\n✅ تم الحفظ في data/last_analysis.json")

main()