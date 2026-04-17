import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("🗃️ خيارات مشكاة")
        
        mode = st.radio(
            "اختر المقام:",
            ["لوحة التحكم", "رادار البصيرة", "إعدادات النظام"]
        )
        
        st.divider()
        st.caption("إصدار السيادة: 1.0.0")
        st.caption("CPU Status: Surah As-Sajdah [5]")
        
        return mode
