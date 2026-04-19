# ============================
#   Mishkat v14 — Root Engine v7.0
#   بدون root_canonizer
# ============================

import streamlit as st
import streamlit.components.v1 as components
import math
import colorsys
import json
import os
import sys
import pandas as pd

from utils.data_loader import load_quran
from utils.root_engine_v7 import analyze_text_v7
from utils.comparison_engine import compare_texts_v12
from utils.gene_spectrum_engine import compute_gene_spectrum_v5
from utils.smart_dome_engine import build_smart_dome_v4
from utils.reasoning_engine import build_reasoning_path_v4
from utils.mesh_engine import build_mesh_networks_v3
from utils.letter_cards import get_letter_card
from utils.fusion_engine import run_full_analysis
from utils.conscious_map_engine import build_conscious_map

st.set_page_config(page_title="Mishkat v14", layout="wide")
st.title("🟣 Mishkat v14 — Root Engine v7.0")
st.caption("جذور قرآنية حقيقية | معجم معتمد | لا تجزئة")

# ============================
#   DATA LOADING
# ============================

def get_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def load_quran_data():
    try:
        path = get_path("data/quran.parquet")
        return pd.read_parquet(path)
    except:
        try:
            from utils.data_loader import load_quran as legacy_load
            return legacy_load()
        except:
            st.error("❌ لم يتم العثور على ملف القرآن")
            return []

quran = load_quran_data()

if isinstance(quran, pd.DataFrame):
    quran = quran.to_dict('records')

# ============================
#   NORMALIZE QURAN KEYS
# ============================

normalized_quran = []
for a in quran:
    entry = {}
    if "surah" in a:
        entry["surah_number"] = int(a["surah"]) if a["surah"] else 0
    elif "surah_number" in a:
        entry["surah_number"] = int(a["surah_number"]) if a["surah_number"] else 0
    else:
        entry["surah_number"] = 0

    if "ayah" in a:
        entry["ayah_number"] = int(a["ayah"]) if a["ayah"] else 0
    elif "ayah_number" in a:
        entry["ayah_number"] = int(a["ayah_number"]) if a["ayah_number"] else 0
    else:
        entry["ayah_number"] = 0

    if "text" in a:
        entry["text"] = a["text"]
    elif "ayah_text" in a:
        entry["text"] = a["ayah_text"]
    else:
        entry["text"] = ""

    normalized_quran.append(entry)

quran = normalized_quran

# ============================
#   GET SURAH ROOTS
# ============================

def get_surah_text(quran, surah_number):
    return " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])

def get_surah_roots_canonical(quran, surah_number):
    from utils.root_engine_v7 import analyze_text_v7

    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v7(text)

    return analysis["root_frequency"]

# ============================
#   MAIN TABS
# ============================

tabs = st.tabs([
    "🧠 الاستعلام الذكي",
    "🧬 تحليل الجذور",
    "🗺️ الخريطة الواعية",
    "🧬 Gene Spectrum v5",
    "🕋 Smart Dome v4",
    "⚖️ المقارنات v12",
    "🧭 الاستدلال v4",
    "🕸 Mesh Networks v3",
    "🗺️ Surah Map v7"
])

# ============================
#   TAB 1
# ============================
with tabs[0]:
    st.subheader("🧠 الاستعلام الذكي")
    q = st.text_area("اكتب سؤالك:", key="search_query")
    if st.button("بحث", key="search_btn") and q.strip():
        result = run_full_analysis(q, quran)
        st.markdown("### 🧬 الجذور")
        st.write(result.get("roots", []))

# ============================
#   TAB 2
# ============================
with tabs[1]:
    st.subheader("🧬 تحليل الجذور")
    text = st.text_area("اكتب نصًا للتحليل:")
    if st.button("تحليل الجذور"):
        analysis = analyze_text_v7(text)
        st.markdown("### 🔤 الجذور المستخرجة")
        st.write(analysis["root_frequency"])

# ============================
#   TAB 3
# ============================
with tabs[2]:
    st.subheader("🗺️ الخريطة الواعية")
    surah_num = st.number_input("اختر السورة:", 1, 114, 1, key="conscious_map")
    if st.button("بناء الخريطة"):
       result = build_conscious_map(quran, surah_num)
        st.markdown("### 🧬 الجذور")
        st.write(result.get("roots", []))

# ============================
#   TAB 4
# ============================
with tabs[3]:
    st.subheader("🧬 Gene Spectrum v5")
    surah_num = st.number_input("اختر السورة:", 1, 114, 1, key="gene_spectrum_v5")
    surah_text = " ".join([a["text"] for a in quran if a["surah_number"] == surah_num])
    spectrum = compute_gene_spectrum_v5(surah_text)
    st.write(spectrum)

# ============================
#   TAB 5
# ============================
with tabs[4]:
    st.subheader("🕋 Smart Dome v4")
    surah_num = st.number_input("اختر السورة:", 1, 114, 1, key="smart_dome_v4")
    dome = build_smart_dome_v4(quran, surah_num)
    st.write(dome)

# ============================
#   TAB 6
# ============================
with tabs[5]:
    st.subheader("⚖️ المقارنات v12")
    text1 = st.text_area("النص الأول:", key="compare_text1")
    text2 = st.text_area("النص الثاني:", key="compare_text2")
    if st.button("قارن") and text1 and text2:
        result = compare_texts_v12(text1, text2)
        st.json(result)

# ============================
#   TAB 7
# ============================
with tabs[6]:
    st.subheader("🧭 الاستدلال")
    text = st.text_area("النص:")
    if st.button("استدل"):
        path = build_reasoning_path_v4(quran, text)
        st.write(path)

# ============================
#   TAB 8
# ============================
with tabs[7]:
    st.subheader("🕸 Mesh Networks v3")
    surah_num = st.number_input("اختر السورة:", 1, 114, 1, key="mesh_v3")
    mesh = build_mesh_networks_v3(quran, surah_num)
    st.write(mesh.get("nodes", []))

# ============================
#   TAB 9
# ============================
with tabs[8]:
    st.subheader("🗺️ Surah Map v7")
    surah_number = st.number_input("اختر رقم السورة:", 1, 114, 1, key="surah_map_v7")
    roots = get_surah_roots_canonical(quran, surah_number)
    
    if roots:
        st.success(f"✅ {len(roots)} جذراً")
        st.write(roots[:30])
    else:
        st.warning("⚠️ لم يتم العثور على جذور")

# ============================
#   FINAL CHECK
# ============================
st.markdown("---")
st.markdown("### ✅ نظام Mishkat v14 جاهز للتشغيل")
