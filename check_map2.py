import json
import re

def normalize(text):
    text = re.sub(r"[ًٌٍَُِّْـٰ]", "", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    return text.strip()

d = json.load(open('data/word_root_map.json', encoding='utf-8'))

# اطبع أول 20 كلمة في الخريطة
print("نماذج من الخريطة:")
for i, (k, v) in enumerate(d.items()):
    print(f"  {k} ← {v}")
    if i >= 20:
        break

# تحقق من كلمات محددة بعد التطبيع
print("\nبحث مع تطبيع:")
words = ['الكتاب', 'كتاب', 'الصلاة', 'صلاه', 'يؤمنون', 'امن', 'الغيب', 'غيب']
for w in words:
    n = normalize(w)
    result = d.get(n, "غير موجود")
    print(f"  {w} → [{n}]: {result}")