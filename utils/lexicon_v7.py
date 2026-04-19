# utils/lexicon_v7.py
import re

def _normalize(text: str) -> str:
    # إزالة التشكيل
    text = re.sub(r"[ًٌٍَُِّْـ]", "", text)
    # توحيد الألف
    text = re.sub(r"[إأآا]", "ا", text)
    return text

# القاموس السيادي للكلمات الحرجة والأدوات
_RAW_SOVEREIGN_LEXICON = {
    "بسم": "سمو",
    "إياك": "أيي",
    "إياكم": "أيي",
    "الذين": "ذوي",
    "نحن": "نفس",
    "اللهم": "أله",
    "اسم": "سمو",
    "الرحمن": "رحم",
    "الرحيم": "رحم",
    "هذا": "هذي",
    "هؤلاء": "أولي",
    "ذلك": "ذلل",
}

SOVEREIGN_LEXICON = {
    _normalize(k): _normalize(v) for k, v in _RAW_SOVEREIGN_LEXICON.items()
}

# حروف الزيادة السطحية (سوابق)
PREFIXES = ['ال', 'بال', 'كال', 'وال', 'فلل', 'ب', 'ف', 'و', 'ل', 'ك']

# لواحق شائعة
SUFFIXES = [
    'كما', 'كما', 'كم', 'هم', 'نا', 'هن', 'كن',
    'تان', 'تين', 'ون', 'ين', 'ات', 'ان', 'ة', 'ه', 'ها'
]

def normalize_token(token: str) -> str:
    return _normalize(token)
