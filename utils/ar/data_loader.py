import json
import streamlit as st

@st.cache_data
def load_quran():
    with open("data/quran.json", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_surah_roots():
    with open("data/surah_roots_index.json", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_roots_mapped():
    with open("data/roots_mapped.json", encoding="utf-8") as f:
        return json.load(f)