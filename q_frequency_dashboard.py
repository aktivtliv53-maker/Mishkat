# q_frequency_dashboard.py
# لوحة تحكم بسيطة لـ Q-Frequency Engine

import json
import streamlit as st
from q_frequency_engine import analyze_verse, LETTER_BANDS

st.set_page_config(page_title="Q-Frequency Engine", layout="wide")

st.title("Q-Frequency Engine — لوحة الترددات القرآنية")

st.markdown("أدخل آية أو نص قرآني لتحليل الترددات الحرفية حسب مدارات الأحرف السبعة.")

default_verse = "يُدَبِّرُ الْأَمْرَ مِنَ السَّمَاءِ إِلَى الْأَرْضِ ثُمَّ يَعْرُجُ إِلَيْهِ فِي يَوْمٍ كَانَ مِقْدَارُهُ أَلْفَ سَنَةٍ مِمَّا تَعُدُّونَ"
verse_input = st.text_area("النص:", value=default_verse, height=120)

if st.button("تحليل الترددات"):
    result = analyze_verse(verse_input)

    st.subheader("ملخص عام")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("مجموع الحروف المصنَّفة", result["total_letters"])
    with col2:
        st.write("المدارات المستخدمة:")
        st.json({k: "".join(v) for k, v in LETTER_BANDS.items()}, expanded=False)

    st.subheader("توزيع المدارات السبعة")
    band_counts = result["counts_per_band"]
    if band_counts:
        st.bar_chart(band_counts)
    else:
        st.info("لا توجد حروف مصنَّفة في هذا النص وفق المجموعات الحالية.")

    st.subheader("توزيع الحروف داخل النص")
    st.json(result["counts_per_letter"], expanded=False)

    st.subheader("النتيجة الخام (JSON)")
    st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")