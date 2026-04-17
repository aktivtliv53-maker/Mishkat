import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def discover_letter_meaning(letter, roots_data):
    matching = [r for r in roots_data if r["root"].startswith(letter) and r["ayah_count"] > 0]
    if len(matching) < 3:
        return None

    top = sorted(matching, key=lambda x: x["ayah_count"], reverse=True)[:15]
    roots_text = "\n".join([f"- {r['root']}: {r['meanings']} ({r['ayah_count']} آية)" for r in top])

    prompt = f"""أنت باحث في اللغة العربية والقرآن الكريم.

هذه الجذور القرآنية التي تبدأ بالحرف "{letter}" مرتبة حسب تكرارها في القرآن:
{roots_text}

من خلال استقراء هذه المعاني مجتمعة:
1. ما المعنى المشترك الذي يجمعها؟
2. ما الوظيفة الجوهرية لهذا الحرف في بنية المعنى العربي؟
3. اقترح وصفاً دقيقاً في جملة واحدة.

لا تستند لأي مرجع خارجي — فقط من هذه الجذور."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "letter": letter,
        "roots_analyzed": len(matching),
        "top_roots": [{"root": r["root"], "meanings": r["meanings"], "ayah_count": r["ayah_count"]} for r in top],
        "discovered_meaning": response.choices[0].message.content
    }

def main():
    data = load_json("data/roots_mapped.json")
    letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    results = []

    for letter in letters:
        print(f"جاري استكشاف حرف: {letter}")
        result = discover_letter_meaning(letter, data)
        if result:
            results.append(result)
            print(f"✓ {letter} — {result['roots_analyzed']} جذر")
            print(result['discovered_meaning'])
            print("---")

    with open("data/letters_discovered.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n✅ تم الحفظ في data/letters_discovered.json")

main()