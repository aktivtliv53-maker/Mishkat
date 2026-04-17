import json
import re

BW = {
    'A':'ا','b':'ب','t':'ت','v':'ث','j':'ج','H':'ح','x':'خ',
    'd':'د','*':'ذ','r':'ر','z':'ز','s':'س','$':'ش','S':'ص',
    'D':'ض','T':'ط','Z':'ظ','E':'ع','g':'غ','f':'ف','q':'ق',
    'k':'ك','l':'ل','m':'م','n':'ن','h':'ه','w':'و','y':'ي',
    'p':'ة','Y':'ى',"'":'ء','>':'أ','<':'إ','&':'ؤ','}':'ئ',
    '|':'آ','W':'ؤ','`':'ا'
}

def bw_to_ar(text):
    return ''.join(BW.get(c, '') for c in text)

def normalize(text):
    text = re.sub(r"[أإآٱؤئ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def parse_corpus(filepath):
    word_root_map = {}
    
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("LOCATION"):
                continue
            
            root_match = re.search(r'ROOT:([A-Za-z*><&}|\'`W]+)', line)
            loc_match = re.match(r'\((\d+):(\d+):(\d+)', line)
            
            if not root_match or not loc_match:
                continue
            
            root_bw = root_match.group(1)
            root_ar = normalize(bw_to_ar(root_bw))
            
            if len(root_ar) < 2:
                continue
            
            surah = loc_match.group(1)
            ayah = loc_match.group(2)
            word_pos = loc_match.group(3)
            
            key = f"{surah}:{ayah}:{word_pos}"
            word_root_map[key] = root_ar
    
    return word_root_map

def main():
    print("جاري التحليل...")
    data = parse_corpus("data/quran-morphology.txt")
    print(f"عدد الكلمات: {len(data)}")
    
    print("\nنماذج:")
    for k, v in list(data.items())[:10]:
        print(f"  {k}: {v}")
    
    json.dump(data, open("data/corpus_roots.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n✅ data/corpus_roots.json")

main()