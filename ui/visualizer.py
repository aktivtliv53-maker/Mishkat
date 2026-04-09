import streamlit as st
from core.mishkat_processor import process_text
from core.force_graph_injection import render_force_graph

def render_visualizer():
    st.title("📡 رادار البصيرة — Mishkat v1.2")

    user_input = st.text_area("أدخل نصًا لتحليل الجذور:", "")

    if st.button("تشغيل الرادار"):
        if not user_input.strip():
            st.warning("الرجاء إدخال نص أولًا.")
            return

        state = process_text(user_input)

        # دمج Q-index داخل العقد
        nodes = []
        for n, q in zip(state["graph_nodes"], state["roots"]):
            n["q_index"] = len(q) * 0.33
            nodes.append(n)

        graph_data = {
            "nodes": nodes,
            "edges": state["graph_edges"]
        }

        st.subheader("🔍 شبكة الجذور")
        render_force_graph(graph_data)

        st.subheader("📊 معلومات التحليل")
        st.write(state)
