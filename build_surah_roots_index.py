import json
import re

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

def main():
    print("جاري التحميل...")
    quran = load_json("data/matrix_data.json")
    corpus = load_json("data/corpus_roots.json")
    roots_data = load_json("data/roots_mapped.json")
    
    roots_index = {normalize(r["root"]): r for r in roots_data}
    
    # بناء فهرس السور
    surah_roots = {}
    
    for ayah in quran:
        s = ayah["surah_number"]
        a = ayah["ayah_number"]
        words = ayah["text"].split()
        
        if s not in surah_roots:
            surah_roots[s] = {}
        
        for i, word in enumerate(words, 1):
            key = f"{s}:{a}:{i}"
            root = corpus.get(key)
            if not root:
                continue
            root_norm = normalize(root)
            if root_norm not in surah_roots[s]:
                surah_roots[s][root_norm] = 0
            surah_roots[s][root_norm] += 1
    
    # تحويل لقائمة مرتبة
    result = {}
    for surah_num, roots in surah_roots.items():
        sorted_roots = sorted(roots.items(), key=lambda x: x[1], reverse=True)
        result[str(surah_num)] = [
            {
                "root": r,
                "count": c,
                "entry": roots_index.get(r, {"root": r, "meanings": "", "ayahs": [], "ayah_count": 0})
            }
            for r, c in sorted_roots
        ]
    
    with open("data/surah_roots_index.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # اختبار على الفاتحة
    print("\nجذور الفاتحة:")
    for r in result["1"][:10]:
        print(f"  {r['root']}: {r['count']}")
    
    print(f"\n✅ تم الحفظ في data/surah_roots_index.json")

main()