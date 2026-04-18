import csv
import json
import streamlit as st

def _safe_int(value, default=0):
    """تحويل آمن إلى integer"""
    if value is None:
        return default
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return default

def _load_csv(path):
    """تحميل ملف CSV مع معالجة الأخطاء"""
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {}
            
            # معالجة رقم السورة
            surah_val = row.get("surah_number") or row.get("surah") or row.get("sura") or 0
            entry["surah_number"] = _safe_int(surah_val)
            
            # معالجة رقم الآية
            ayah_val = row.get("ayah_number") or row.get("ayah") or row.get("aya") or 0
            entry["ayah_number"] = _safe_int(ayah_val)
            
            # معالجة النص
            entry["text"] = row.get("text") or row.get("ayah_text") or ""
            
            data.append(entry)
    return data

def _load_json(path):
    """تحميل ملف JSON"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # توحيد المفاتيح إذا كانت مختلفة
    normalized = []
    for item in data:
        entry = {}
        entry["surah_number"] = _safe_int(item.get("surah_number") or item.get("surah") or 0)
        entry["ayah_number"] = _safe_int(item.get("ayah_number") or item.get("ayah") or 0)
        entry["text"] = item.get("text") or item.get("ayah_text") or ""
        normalized.append(entry)
    
    return normalized

def _load_quran_file(path):
    """تحميل ملف القرآن حسب امتداده"""
    if path.endswith(".csv"):
        return _load_csv(path)
    else:
        return _load_json(path)

@st.cache_data
def load_quran(path=None):
    """تحميل ملف القرآن (يدعم csv أو json) مع اكتشاف تلقائي"""
    if path is None:
        # محاولة تحميل csv أولاً
        try:
            return _load_csv("data/quran.csv")
        except FileNotFoundError:
            pass
        
        # محاولة تحميل json ثانياً
        try:
            return _load_json("data/quran.json")
        except FileNotFoundError:
            pass
        
        # إذا لم يتم العثور على أي ملف
        raise FileNotFoundError("لم يتم العثور على ملف القرآن في data/quran.csv أو data/quran.json")
    else:
        return _load_quran_file(path)
