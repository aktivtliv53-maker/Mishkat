import streamlit as st
from core.force_graph_injection import render_force_graph

def render_visualizer(data=None):
    # بيانات اختبار صلبة لا تقبل الشك
    test_data = {
        "nodes": [{"id": "1", "label": "نور", "semantic_phase": "light"}],
        "edges": []
    }
    st.write("📡 محاولة الاتصال بالرادار...")
    render_force_graph(test_data)
