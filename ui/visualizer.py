import streamlit as st
from core.mishkat_processor import process_text
from core.force_graph_injection import render_force_graph

def render_visualizer():
    st.title("📡 رادار البصيرة — Mishkat")

    user_input = st.text_area("أدخل نصًا لتحليل الجذور:", "")

    if st.button("تشغيل الرادار"):
        if not user_input.strip():
            st.warning("الرجاء إدخال نص أولًا.")
            return

        # 1) تحليل النص عبر معالج مشكاة الحقيقي
        state = process_text(user_input)

        # 2) استخراج بيانات الشبكة
        graph_data = {
            "nodes": state["graph_nodes"],
            "edges": state["graph_edges"]
        }

        # 3) عرض الشبكة
        st.subheader("🔍 شبكة الجذور")
        render_force_graph(graph_data)

        # 4) عرض معلومات إضافية
        st.subheader("📊 معلومات التحليل")
        st.write(state)
