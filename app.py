import streamlit as st
from ui import mode_single, mode_compare, mode_dashboard

# إعداد الصفحة بهوية "مشكاة"
st.set_page_config(page_title="Mishkat v100", layout="wide", page_icon="💡")

# الهوية البصرية السيادية لنظام مشكاة
st.sidebar.title("💡 نظام مشكاة (Mishkat)")
st.sidebar.markdown("*نور على نور - للهندسة الوجودية*")
st.sidebar.markdown("---")

# اختيار مسار الوعي
choice = st.sidebar.radio(
    "اختر مدار البحث:",
    ["التحليل الفردي (Single)", "مقارنة المدارات (Compare)", "لوحة القيادة (Dashboard)"]
)

# الربط بين الاختيار والواجهات
if choice == "التحليل الفردي (Single)":
    mode_single.run()
elif choice == "مقارنة المدارات (Compare)":
    mode_compare.run()
else:
    mode_dashboard.run()

st.sidebar.markdown("---")
st.sidebar.info("بعلم مكين نسخر خلاصة التمكين")
st.sidebar.caption("Mishkat Sovereign System © 2026")
