import streamlit as st
from core.force_graph_injection import render_force_graph

def render_visualizer(state_data=None):
    st.subheader("🔭 رادار البصيرة")
    
    if state_data:
        # تحويل بيانات الحالة إلى تنسيق شبكة بسيط للعرض
        graph_data = {
            "nodes": [
                {"id": state_data["id"], "label": state_data["label"], "semantic_phase": state_data["semantic_phase"]}
            ],
            "edges": []
        }
        render_force_graph(graph_data)
    else:
        st.info("قم بإدخال بيانات في لوحة التحكم لبدء المحاكاة البصرية.")
