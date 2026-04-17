import streamlit as st
import json

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

st.set_page_config(page_title="مِشكاة — الحروف", layout="wide", page_icon="🕌")

st.title("🕌 مِشكاة — خريطة الحروف القرآنية")
st.markdown("بيانات مستخرجة من القرآن الكريم مباشرة")

data = load_json("data/final_letter_table.json")
letters = data["letter_table"]
ta_theory = data["ta_theory"]

# فلتر المجال
domains = list(set(l["المجال_الغالب"] for l in letters))
selected_domain = st.sidebar.selectbox("فلتر بالمجال", ["الكل"] + sorted(domains))

# فلتر الموقع
positions = ["الكل", "بداية", "وسط", "نهاية"]
selected_position = st.sidebar.selectbox("الموقع الغالب", positions)

# تصفية البيانات
filtered = letters
if selected_domain != "الكل":
    filtered = [l for l in filtered if l["المجال_الغالب"] == selected_domain]

if selected_position != "الكل":
    def is_dominant(letter, pos):
        b = float(letter["بداية"].replace("%",""))
        m = float(letter["وسط"].replace("%",""))
        n = float(letter["نهاية"].replace("%",""))
        if pos == "بداية": return b == max(b,m,n)
        if pos == "وسط": return m == max(b,m,n)
        if pos == "نهاية": return n == max(b,m,n)
    filtered = [l for l in filtered if is_dominant(l, selected_position)]

# عرض البطاقات
st.markdown(f"### عدد الحروف: {len(filtered)}")

cols = st.columns(4)
for i, letter in enumerate(filtered):
    with cols[i % 4]:
        val = letter["القيمة_الوظيفية"]
        color = "#ff5722" if val > 0.96 else "#1976d2" if val > 0.93 else "#388e3c"
        
        st.markdown(f"""
        <div style="
            background: {color}15;
            border: 2px solid {color};
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            text-align: center;
        ">
            <h1 style="font-size:3rem; margin:0; color:{color}">{letter['الحرف']}</h1>
            <p style="margin:4px 0; font-size:0.9rem"><b>الجذور:</b> {letter['عدد_الجذور']}</p>
            <p style="margin:4px 0; font-size:0.9rem"><b>المجال:</b> {letter['المجال_الغالب']}</p>
            <p style="margin:4px 0; font-size:0.85rem">
                بداية {letter['بداية']} | وسط {letter['وسط']} | نهاية {letter['نهاية']}
            </p>
            <p style="margin:4px 0; font-size:0.8rem; color:{color}"><b>{letter['أعلى_الجذور']}</b></p>
        </div>
        """, unsafe_allow_html=True)

# تفاصيل الحرف
st.markdown("---")
st.subheader("🔍 تفاصيل حرف")
selected_letter = st.selectbox("اختر حرفاً", [l["الحرف"] for l in letters])
detail = next(l for l in letters if l["الحرف"] == selected_letter)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("عدد الجذور", detail["عدد_الجذور"])
    st.metric("القيمة الوظيفية", detail["القيمة_الوظيفية"])
with col2:
    st.metric("المجال الغالب", detail["المجال_الغالب"])
    st.metric("الموقع الغالب", 
        "بداية" if float(detail["بداية"].replace("%","")) == max(
            float(detail["بداية"].replace("%","")),
            float(detail["وسط"].replace("%","")),
            float(detail["نهاية"].replace("%",""))
        ) else "وسط" if float(detail["وسط"].replace("%","")) == max(
            float(detail["بداية"].replace("%","")),
            float(detail["وسط"].replace("%","")),
            float(detail["نهاية"].replace("%",""))
        ) else "نهاية"
    )
with col3:
    if detail.get("دور_صرفي_بداية"):
        st.metric("دور صرفي (بداية)", detail["دور_صرفي_بداية"])
    if detail.get("دور_صرفي_نهاية"):
        st.metric("دور صرفي (نهاية)", detail["دور_صرفي_نهاية"])

st.markdown(f"**أعلى الجذور:** {detail['أعلى_الجذور']}")

# نظرية التاء
st.markdown("---")
st.subheader("📊 نظرية التاء — مثبتة من القرآن")
st.info(ta_theory["conclusion"])

cols_ta = st.columns(len(ta_theory["summary"]))
for i, (cat, count) in enumerate(sorted(ta_theory["summary"].items(), key=lambda x: x[1], reverse=True)):
    total = sum(ta_theory["summary"].values())
    with cols_ta[i]:
        st.metric(cat, f"{count}", f"{count/total*100:.1f}%")