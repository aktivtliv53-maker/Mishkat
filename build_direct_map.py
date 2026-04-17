import json
import re

BW = {
    'A':'ا','b':'ب','t':'ت','v':'ث','j':'ج','H':'ح','x':'خ',
    'd':'د','*':'ذ','r':'ر','z':'ز','s':'س','$':'ش','S':'ص',
    'D':'ض','T':'ط','Z':'ظ','E':'ع','g':'غ','f':'ف','q':'ق',
    'k':'ك','l':'ل','m':'م','n':'ن','h':'ه','w':'و','y':'ي',
    "'":"ء",'>':'أ','<':'إ','&':'ؤ','}':'ئ','Y':'ى','p':'ة'
}

def bw_to_ar(text):
    return ''.join(BW.get(c, '') for c in text)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱؤئ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def main():
    print("جاري البناء...")
    word_root_map = {}
    
    with open("data/quran-morphology.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("LOCATION"):
                continue
            
            # استخراج الجذر
            root_match = re.search(r'ROOT:([A-Za-z*><&}\']+)', line)
            if not root_match:
                continue
            root_ar = normalize(bw_to_ar(root_match.group(1)))
            if len(root_ar) < 2:
                continue
            
            # استخراج شكل الكلمة (LEM)
            lem_match = re.search(r'LEM:([^\|]+)', line)
            if lem_match:
                lem_bw = lem_match.group(1)
                lem_ar = normalize(bw_to_ar(lem_bw))
                if len(lem_ar) >= 2:
                    word_root_map[lem_ar] = root_ar
            
            # استخراج شكل الكلمة الخام (العمود الثاني)
            parts = line.split('\t')
            if len(parts) >= 2:
                form_bw = parts[1]
                form_ar = normalize(bw_to_ar(form_bw))
                if len(form_ar) >= 2:
                    if form_ar not in word_root_map:
                        word_root_map[form_ar] = root_ar
    
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    test = ["الكتاب","للمتقين","يؤمنون","الغيب","الصلاة","الرحيم","رزقناهم","يعلمون","ذلك","كتاب","رحم","صلاه"]
    print("\nاختبار:")
    found = 0
    for word in test:
        r = word_root_map.get(normalize(word), "—")
        if r != "—":
            print(f"  ✓ {word} ← {r}")
            found += 1
        else:
            print(f"  ✗ {word}")
    
    print(f"\n{found}/{len(test)} ({found/len(test)*100:.1f}%)")
    
    json.dump(word_root_map, open("data/word_to_root.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/word_to_root.json")

main()