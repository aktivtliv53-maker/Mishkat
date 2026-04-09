import streamlit as st
from ui.visualizer import render_visualizer
from ui.dashboard import render_dashboard

st.sidebar.title("✨ Mishkat Navigation v1.1")
choice = st.sidebar.radio("اختر وضع التشغيل:", ["الرادار", "لوحة التحكم"])

if choice == "الرادار":
    render_visualizer()
else:
    render_dashboard()
