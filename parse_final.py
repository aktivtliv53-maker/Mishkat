import json
import re

BW = {
    'A':'ا','b':'ب','t':'ت','v':'ث','j':'ج','H':'ح','x':'خ',
    'd':'د','*':'ذ','r':'ر','z':'ز','s':'س','$':'ش','S':'ص',
    'D':'ض','T':'ط','Z':'ظ','E':'ع','g':'غ','f':'ف','q':'ق',
    'k':'ك','l':'ل','m':'م','n':'ن','h':'ه','w':'و','y':'ي',
    "'":"ء",'>':'أ','<':'إ','&':'ؤ','}':'ئ','|':'آ','Y':'ى',
    'p':'ة','~':'','`':'','F':'','N':'','K':'','a':'','u':'',
    'i':'','o':'','W':'و'
}

def bw_to_ar(text):
    return ''.join(BW.get(c, '') for c in text)

def normalize(text):
    text = re.sub(r"[أإآٱؤئ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def main():
    print("جاري التحليل...")
    word_root_map = {}
    
    with open("data/quran-morphology.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("LOCATION"):
                continue
            
            # استخراج الموقع
            loc = re.match(r'\((\d+):(\d+):(\d+):\d+\)', line)
            if not loc:
                continue
            
            surah = loc.group(1)
            ayah = loc.group(2)
            word = loc.group(3)
            key = f"{surah}:{ayah}:{word}"
            
            # استخراج الجذر
            root_match = re.search(r'ROOT:([A-Za-z*><&}|\']+)', line)
            if not root_match:
                continue
            
            root_bw = root_match.group(1)
            root_ar = normalize(bw_to_ar(root_bw))
            
            if len(root_ar) >= 2:
                word_root_map[key] = root_ar
    
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    # اختبار
    print("\nنماذج:")
    test = ["2:2:2", "2:2:4", "2:2:6", "2:2:7", "1:1:2", "1:2:3"]
    expected = {"2:2:2":"كتب", "2:2:4":"ريب", "2:2:6":"هدي", "2:2:7":"وقي"}
    for k in test:
        v = word_root_map.get(k, "—")
        exp = expected.get(k, "")
        status = "✓" if not exp or v == exp else "✗"
        print(f"  {status} {k}: {v} {f'(متوقع: {exp})' if exp else ''}")
    
    json.dump(word_root_map, open("data/corpus_roots.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/corpus_roots.json")

main()