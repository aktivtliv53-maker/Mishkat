import streamlit as st
from core.mishkat_db import get_all_sessions

def render_dashboard():
    st.title("🛡️ لوحة التحكم السيادية")
    
    sessions_df = get_all_sessions()
    
    if not sessions_df.empty:
        st.subheader("المسارات الأخيرة")
        for index, row in sessions_df.iterrows():
            with st.expander(f"📌 {row['title']} - {row['timestamp']}"):
                st.write(f"**المحتوى:** {row['content']}")
                st.info(f"الطور الدلالي: {row['phase']}")
    else:
        st.write("لا توجد مسارات مسجلة حتى الآن. ابدأ بإنشاء أول مسار لك.")
