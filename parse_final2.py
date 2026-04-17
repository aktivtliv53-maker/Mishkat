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
            
            loc = re.match(r'\((\d+):(\d+):(\d+):\d+\)', line)
            if not loc:
                continue
            
            key = f"{loc.group(1)}:{loc.group(2)}:{loc.group(3)}"
            
            root_match = re.search(r'ROOT:([A-Za-z*><&}\']+)', line)
            if not root_match:
                continue
            
            root_bw = root_match.group(1)
            root_ar = normalize(bw_to_ar(root_bw))
            
            if len(root_ar) >= 2:
                word_root_map[key] = root_ar
    
    print(f"عدد الكلمات: {len(word_root_map)}")
    
    test = {
        "2:2:2":"كتب","2:2:4":"ريب","2:2:6":"هدي",
        "2:2:7":"وقي","1:1:2":"اله","1:2:3":"ربب"
    }
    print("\nاختبار:")
    for k, exp in test.items():
        v = word_root_map.get(k, "—")
        print(f"  {'✓' if v==exp else '✗'} {k}: {v} (متوقع: {exp})")
    
    json.dump(word_root_map, open("data/corpus_roots.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/corpus_roots.json")

main()