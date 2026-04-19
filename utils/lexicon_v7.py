# ============================
#   Lexicon v7.0 — القاموس الجذري للقرآن
#   يحتوي على الجذور الصحيحة مع معانيها وأوزانها
# ============================

LEXICON_V7 = {
    # الجذور الثلاثية الأساسية
    "سمو": {"meaning": "العلو والارتفاع", "weight": 0.95, "category": "علوي"},
    "اله": {"meaning": "الألوهية والعبادة", "weight": 0.98, "category": "توحيد"},
    "رحم": {"meaning": "الرحمة والعطف", "weight": 0.97, "category": "رحمة"},
    "حمد": {"meaning": "الشكر والثناء", "weight": 0.94, "category": "عبادة"},
    "ربب": {"meaning": "التربية والسيادة", "weight": 0.96, "category": "توحيد"},
    "علم": {"meaning": "المعرفة والإدراك", "weight": 0.93, "category": "علم"},
    "ملك": {"meaning": "الملك والسيطرة", "weight": 0.92, "category": "قوة"},
    "يوم": {"meaning": "الزمن والوقت", "weight": 0.89, "category": "زمن"},
    "دين": {"meaning": "الجزاء والطاعة", "weight": 0.91, "category": "تشريع"},
    "عبد": {"meaning": "العبادة والخضوع", "weight": 0.96, "category": "عبادة"},
    "عون": {"meaning": "المساعدة والنصر", "weight": 0.88, "category": "فعل"},
    "هدي": {"meaning": "الإرشاد والدلالة", "weight": 0.94, "category": "هداية"},
    "صرط": {"meaning": "الطريق المستقيم", "weight": 0.90, "category": "طريق"},
    "قوم": {"meaning": "الاستقامة والنهوض", "weight": 0.87, "category": "حركة"},
    "علو": {"meaning": "الارتفاع والسمو", "weight": 0.85, "category": "علوي"},
    "نعم": {"meaning": "النعمة والإحسان", "weight": 0.92, "category": "نعمة"},
    "غير": {"meaning": "المخالفة والاختلاف", "weight": 0.83, "category": "مقارنة"},
    "غضب": {"meaning": "السخط والعقاب", "weight": 0.86, "category": "عقاب"},
    "ضلل": {"meaning": "الضلال والانحراف", "weight": 0.84, "category": "انحراف"},
    "كفر": {"meaning": "الجحود والإنكار", "weight": 0.88, "category": "عقيدة"},
    "امن": {"meaning": "الأمان والإيمان", "weight": 0.95, "category": "عقيدة"},
    "نزل": {"meaning": "النزول والتنزيل", "weight": 0.86, "category": "فعل"},
    "قبل": {"meaning": "السبق والتقدم", "weight": 0.84, "category": "زمن"},
    "اخر": {"meaning": "التأخر والآخرة", "weight": 0.87, "category": "زمن"},
    "يقن": {"meaning": "اليقين والثقة", "weight": 0.89, "category": "علم"},
    "فلح": {"meaning": "الفلاح والنجاح", "weight": 0.88, "category": "نجاح"},
    "نذر": {"meaning": "الإنذار والتحذير", "weight": 0.82, "category": "تواصل"},
    "ختم": {"meaning": "الختم والإغلاق", "weight": 0.80, "category": "فعل"},
    "قلب": {"meaning": "تقلب القلب", "weight": 0.85, "category": "نفسي"},
    "سمع": {"meaning": "السمع والإنصات", "weight": 0.87, "category": "حواس"},
    "بصر": {"meaning": "البصر والرؤية", "weight": 0.86, "category": "حواس"},
    "عذب": {"meaning": "العذاب والألم", "weight": 0.84, "category": "عقاب"},
    "عظم": {"meaning": "العظمة والكبر", "weight": 0.85, "category": "صفات"},
    "خدع": {"meaning": "الخداع والمكر", "weight": 0.78, "category": "سلوك"},
}

def get_root_info(root):
    """الحصول على معلومات الجذر من القاموس"""
    return LEXICON_V7.get(root, {"meaning": "غير معروف", "weight": 0.5, "category": "عام"})

def get_root_weight(root):
    """الحصول على وزن الجذر"""
    return get_root_info(root)["weight"]

def get_root_category(root):
    """الحصول على فئة الجذر"""
    return get_root_info(root)["category"]

def get_root_meaning(root):
    """الحصول على معنى الجذر"""
    return get_root_info(root)["meaning"]
