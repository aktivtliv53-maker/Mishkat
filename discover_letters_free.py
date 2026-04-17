import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def discover_letter_free(letter, roots_data):
    matching = [r for r in roots_data if r["root"].startswith(letter) and r["ayah_count"] > 0]
    if len(matching) < 3:
        return None

    top = sorted(matching, key=lambda x: x["ayah_count"], reverse=True)[:10]
    
    ayahs_text = ""
    for root in top:
        ayahs_text += f"\n[جذر: {root['root']}]\n"
        for ayah in root["ayahs"][:3]:
            ayahs_text += f"- {ayah['text']}\n"

    prompt = f"""هذه آيات قرآنية تبدأ جذورها بالحرف "{letter}":

{ayahs_text}

ماذا تلاحظ؟"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "letter": letter,
        "roots_count": len(matching),
        "raw_observation": response.choices[0].message.content
    }

def main():
    data = load_json("data/roots_mapped.json")
    letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    results = []

    for letter in letters:
        print(f"جاري استكشاف حرف: {letter}")
        result = discover_letter_free(letter, data)
        if result:
            results.append(result)
            print(f"✓ {letter}")
            print(result['raw_observation'])
            print("---")

    with open("data/letters_free.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n✅ تم الحفظ في data/letters_free.json")

main()