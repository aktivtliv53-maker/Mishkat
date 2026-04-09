import streamlit as st
from core.mishkat_orchestrator import MishkatSystem
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.visualizer import render_visualizer

# إعدادات الصفحة السيادية
st.set_page_config(
    page_title="مشكاة: النظام السيادي",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة النظام
if "mishkat" not in st.session_state:
    st.session_state.mishkat = MishkatSystem()

def main():
    # 1. رصد الهوية والجانب (Sidebar)
    menu_choice = render_sidebar()

    # 2. منطقة العمل الرئيسية
    if menu_choice == "لوحة التحكم":
        st.title("🛡️ لوحة التحكم السيادية")
        render_dashboard()
        
    elif menu_choice == "المحرك البصري":
        st.title("🌐 رادار المدارات المقلوبة")
        # بيانات تجريبية للمحرك البصري حتى يتم ربط القاعدة بالكامل
        sample_data = {
            "nodes": [
                {"id": "نور", "label": "نور", "semantic_phase": "light"},
                {"id": "قدر", "label": "قدر", "semantic_phase": "power"},
                {"id": "زكي", "label": "زكي", "semantic_phase": "purification"}
            ],
            "edges": [
                {"source": "نور", "target": "قدر", "weight": 2},
                {"source": "قدر", "target": "زكي", "weight": 1}
            ]
        }
        render_visualizer(sample_data)

    elif menu_choice == "إعدادات النظام":
        st.title("⚙️ إعدادات مشكاة")
        st.write(f"إصدار النظام: {st.session_state.mishkat.version}")
        st.info("النظام يعمل الآن بكامل طاقته السيادية.")

if __name__ == "__main__":
    main()
