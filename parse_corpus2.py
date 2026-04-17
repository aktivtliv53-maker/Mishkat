import json
import re

def parse_corpus(filepath):
    word_root_map = {}
    
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("LOCATION"):
                continue
            
            root_match = re.search(r'ROOT:([^\|]+)', line)
            loc_match = re.match(r'\((\d+):(\d+):(\d+)', line)
            
            if not root_match or not loc_match:
                continue
            
            root = root_match.group(1).split('|')[0].strip()
            surah = loc_match.group(1)
            ayah = loc_match.group(2)
            word_pos = loc_match.group(3)
            
            key = f"{surah}:{ayah}:{word_pos}"
            word_root_map[key] = root
    
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