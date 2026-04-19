import streamlit as st
import pandas as pd
import altair as alt
import os, sys, json, colorsys

from utils.data_loader import load_quran
from utils.root_engine_v7 import analyze_text_v7
from utils.comparison_engine import compare_texts_v12
from utils.gene_spectrum_engine import compute_gene_spectrum_v5
from utils.smart_dome_engine import build_smart_dome_v4
from utils.reasoning_engine import build_reasoning_path_v4
from utils.mesh_engine import build_mesh_networks_v3
from utils.letter_cards import get_letter_card
from utils.fusion_engine import run_full_analysis
from utils.conscious_map_engine import build_conscious_map
from utils.surah_map_engine import build_surah_map

st.set_page_config(page_title="Mishkat v14", layout="wide")
st.title("🟣 Mishkat v14 — Root Engine v7.0")

def get_path(rel):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)

def load_quran_data():
    try:
        return pd.read_parquet(get_path("data/quran.parquet"))
    except:
        try:
            return load_quran()
        except:
            st.error("❌ ملف القرآن غير موجود")
            return []

quran = load_quran_data()
if isinstance(quran, pd.DataFrame):
    quran = quran.to_dict("records")

normalized = []
for a in quran:
    normalized.append({
        "surah_number": int(a.get("surah") or a.get("surah_number") or 0),
        "ayah_number": int(a.get("ayah") or a.get("ayah_number") or 0),
        "text": a.get("text") or a.get("ayah_text") or ""
    })
quran = normalized

def get_surah_text(q, s):
    return " ".join([a["text"] for a in q if a["surah_number"] == s])

def get_surah_roots_canonical(q, s):
    return analyze_text_v7(get_surah_text(q, s))["root_frequency"]

tabs = st.tabs([
    "🧠 الاستعلام الذكي",
    "🧬 تحليل الجذور",
    "🗺️ الخريطة الواعية",
    "🧬 Gene Spectrum v5",
    "🕋 Smart Dome v4",
    "⚖️ المقارنات v12",
    "🧭 الاستدلال v4",
    "🕸 Mesh Networks v3",
    "🗺️ Surah Map v7"
])

with tabs[0]:
    st.subheader("🧠 الاستعلام الذكي")
    q = st.text_area("اكتب سؤالك:")
    if st.button("بحث"):
        if not q.strip():
            st.warning("⚠️ اكتب سؤالًا")
        else:
            r = run_full_analysis(quran, 1, q)
            st.write(r.get("text_root_analysis", {}))
            st.info(r.get("state", ""))
            st.success(r.get("guidance", ""))

with tabs[1]:
    st.subheader("🧬 تحليل الجذور")
    t = st.text_area("اكتب نصًا:")
    if st.button("تحليل"):
        a = analyze_text_v7(t)
        st.dataframe(a["root_frequency"])
        df = pd.DataFrame(a["root_frequency"], columns=["root", "count"])
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(x="root", y="count"), 
            use_container_width=True
        )

with tabs[2]:
    st.subheader("🗺️ الخريطة الواعية")
    s = st.number_input("السورة:", 1, 114, 1)
    if st.button("بناء"):
        st.dataframe(build_conscious_map(quran, s).get("levels", []))

with tabs[3]:
    st.subheader("🧬 Gene Spectrum v5")
    s = st.number_input("السورة:", 1, 114, 1, key="g")
    st.write(compute_gene_spectrum_v5(get_surah_text(quran, s)))

with tabs[4]:
    st.subheader("🕋 Smart Dome v4")
    s = st.number_input("السورة:", 1, 114, 1, key="d")
    st.write(build_smart_dome_v4(quran, s))

with tabs[5]:
    st.subheader("⚖️ المقارنات v12")
    t1 = st.text_area("النص الأول:")
    t2 = st.text_area("النص الثاني:")
    if st.button("قارن"):
        if t1 and t2:
            st.json(compare_texts_v12(t1, t2))
        else:
            st.warning("⚠️ أدخل النصين")

with tabs[6]:
    st.subheader("🧭 الاستدلال")
    t = st.text_area("النص:")
    if st.button("استدل"):
        st.write(build_reasoning_path_v4(quran, t))

with tabs[7]:
    st.subheader("🕸 Mesh Networks v3")
    s = st.number_input("السورة:", 1, 114, 1, key="m")
    st.write(build_mesh_networks_v3(quran, s).get("nodes", []))

# ============================
#   SURAH MAP v7 (FINAL)
# ============================

def weight_to_color(w):
    hue = 0.6
    sat = 0.5
    light = max(0.2, 0.8 - (w * 0.05))
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

def cluster_root(r):
    if r.startswith("ق"): return "Qaf"
    if r.startswith("م"): return "Meem"
    if r.startswith("ا"): return "Alif"
    return "Other"

with tabs[8]:
    st.subheader("🗺️ Surah Map v7")

    s = st.number_input("رقم السورة:", 1, 114, 1)
    min_w = st.slider("أقل تكرار للجذر:", 1, 10, 3)

    if st.button("عرض الخريطة"):
        r = build_surah_map(quran, s)

        from streamlit_agraph import agraph, Node, Edge, Config

        fn = [n for n in r["nodes"] if n["weight"] >= min_w]
        allowed = set([n["id"] for n in fn])
        fl = [l for l in r["links"] if l["source"] in allowed and l["target"] in allowed]

        nodes = [
            Node(
                id=n["id"],
                label=n["id"],
                size=n["weight"] * 3,
                color=weight_to_color(n["weight"]),
                group=cluster_root(n["id"])
            )
            for n in fn
        ]

        edges = [
            Edge(
                source=l["source"],
                target=l["target"],
                label=str(l["weight"])
            )
            for l in fl
        ]

        config = Config(
            width=900,
            height=600,
            directed=False,
            physics=True,
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#FFD700",
            collapsible=False
        )

        try:
            agraph(nodes=nodes, edges=edges, config=config)
        except Exception as e:
            st.error(f"خطأ: {e}")

st.markdown("---")
st.markdown("### ✅ Mishkat v14 جاهز")

try:
    roots = get_surah_roots_canonical(quran, 1)
    st.success(f"✔ Root Engine يعمل — {len(roots)} جذراً")
except Exception as e:
    st.error(f"❌ خطأ: {e}")
