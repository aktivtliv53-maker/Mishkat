import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def get_root_concept(root, meanings, ayahs):
    ayah_texts = "\n".join([f"- {a['text']}" for a in ayahs[:20]])
    
    prompt = f"""أنت باحث في اللغة القرآنية.
الجذر: {root}
المعنى الأساسي: {meanings}

الآيات التي ورد فيها هذا الجذر:
{ayah_texts}

استخلص المفهوم القرآني الجوهري لهذا الجذر من خلال تقاطع هذه الآيات.
أجب في جملتين فقط."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# تجربة على جذر واحد
data = load_json("roots_mapped.json")

for entry in data:
    if entry["root"] == "كتب" and entry["ayah_count"] > 0:
        concept = get_root_concept(
            entry["root"],
            entry["meanings"],
            entry["ayahs"]
        )
        print(f"الجذر: {entry['root']}")
        print(f"عدد الآيات: {entry['ayah_count']}")
        print(f"المفهوم القرآني: {concept}")
        break