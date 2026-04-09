import streamlit as st
from core.force_graph_injection import render_force_graph

def render_visualizer(data=None):
    st.subheader("🌐 رادار المدارات المقلوبة")
    
    if data is None:
        # بيانات افتراضية لضمان عمل المحرك عند الاختبار الأول
        data = {
            "nodes": [
                {"id": "نور", "label": "نور", "group": 1, "semantic_phase": "light"},
                {"id": "قدر", "label": "قدر", "group": 2, "semantic_phase": "power"},
                {"id": "زكي", "label": "زكي", "group": 3, "semantic_phase": "purification"}
            ],
            "edges": [
                {"source": "نور", "target": "قدر", "weight": 2},
                {"source": "قدر", "target": "زكي", "weight": 1}
            ]
        }

    # عرض عداد للتأكد من وصول البيانات
    col1, col2 = st.columns(2)
    col1.metric("عدد النقاط (Nodes)", len(data["nodes"]))
    col2.metric("عدد الروابط (Edges)", len(data["edges"]))

    # استدعاء الحقن البرمجي للرادار
    try:
        render_force_graph(data)
    except Exception as e:
        st.error(f"حدث خطأ أثناء تشغيل المحرك البصري: {e}")

    st.caption("تلميح: استخدم الماوس لتدوير الشبكة، والعجلة للتكبير.")
