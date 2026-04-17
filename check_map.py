import json

d = json.load(open('data/word_root_map.json', encoding='utf-8'))
words = ['الكتاب','كتاب','للمتقين','متقين','الصلاة','صلاه','الغيب','غيب','يؤمنون','امن']

for w in words:
    result = d.get(w, "غير موجود")
    print(f"{w}: {result}")