import json
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def analyze_letter_deep(letter, roots_data):
    matching = [r for r in roots_data if r["root"].startswith(letter) and r["ayah_count"] > 0]
    if not matching:
        return None

    top = sorted(matching, key=lambda x: x["ayah_count"], reverse=True)[:8]
    results = []

    for root in top:
        ayahs = root["ayahs"][:5]
        ayahs_text = "\n".join([f"- {a['surah']} ({a['ayah_number']}): {a['text']}" for a in ayahs])

        prompt = f"""هذه آيات قرآنية تحتوي على جذر "{root['root']}":

{ayahs_text}

ما الذي تكشفه هذه الآيات عن معنى هذا الجذر؟ اكتب ملاحظة واحدة دقيقة فقط."""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            observation = response.choices[0].message.content
        except Exception as e:
            print(f"خطأ: {e}")
            observation = "تعذر التحليل"

        results.append({
            "root": root["root"],
            "ayah_count": root["ayah_count"],
            "observation": observation
        })

        print(f"  ✓ {root['root']} ({root['ayah_count']} آية)")
        time.sleep(3)

    # الاستخلاص النهائي
    all_observations = "\n".join([f"- {r['root']}: {r['observation']}" for r in results])

    final_prompt = f"""أنت باحث في اللغة العربية.

هذه ملاحظات مستخلصة من آيات قرآنية لجذور تبدأ بالحرف "{letter}":

{all_observations}

من خلال هذه الجذور مجتمعة، ما الدور الجوهري الذي يؤديه الحرف "{letter}" في بنية المعنى العربي؟

اكتب إجابة عميقة ونهائية في فقرة واحدة فقط."""

    time.sleep(5)
    final = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": final_prompt}]
    )

    return {
        "letter": letter,
        "roots_analyzed": results,
        "final_meaning": final.choices[0].message.content
    }

def main():
    data = load_json("data/roots_mapped.json")
    letter = input("أدخل الحرف المراد تحليله: ").strip()

    print(f"\nجاري التحليل العميق للحرف: {letter}")
    result = analyze_letter_deep(letter, data)

    if result:
        print(f"\n{'='*50}")
        print(f"الحرف: {letter}")
        print(f"{'='*50}")
        print(f"\nالمعنى الجوهري النهائي:\n{result['final_meaning']}")

        output_path = f"data/letter_{letter}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ تم الحفظ في {output_path}")

main()