import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
import os

# ---------------------------------------------------
# المسارات وتحميل البيانات
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOTS_PATH = os.path.join(BASE_DIR, "data", "roots_mapped.json")

def load_roots(path=ROOTS_PATH):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

ROOTS_DATA = load_roots()

def get_root_entry(root):
    for entry in ROOTS_DATA:
        if entry.get("root") == root:
            return entry
    return None

# ---------------------------------------------------
# حساب المقاييس الأساسية + الوزن المفهومي
# ---------------------------------------------------
def compute_root_metrics(entry):
    if not entry:
        return {
            "strength": 0,
            "spread": 0,
            "diversity": 0.0,
            "avg_ayah_len": 0.0,
            "context_density": 0.0,
            "concept_weight": 0.0,
        }

    ayahs = entry.get("ayahs", [])
    strength = len(ayahs)
    surahs = set()
    all_words = []
    ayah_lengths = []

    for a in ayahs:
        surahs.add(a.get("surah_number"))
        text = a.get("text", "")
        words = text.split()
        all_words.extend(words)
        ayah_lengths.append(len(words))

    spread = len(surahs)
    unique_words = set(all_words)
    total_words = len(all_words)

    diversity = len(unique_words) / total_words if total_words > 0 else 0.0
    avg_ayah_len = sum(ayah_lengths) / len(ayah_lengths) if ayah_lengths else 0.0
    context_density = len(unique_words) / (strength + 1e-6) if strength > 0 else 0.0

    # وزن مفهومي مبسّط (يمكن تطويره لاحقًا)
    # مزيج من: قوة الحضور + الانتشار + التنوع + كثافة السياق
    w_strength = np.tanh(strength / 80.0)
    w_spread = np.tanh(spread / 20.0)
    w_div = np.clip(diversity * 4.0, 0, 1)
    w_ctx = np.clip(context_density / 10.0, 0, 1)

    concept_weight = (0.35 * w_strength +
                      0.25 * w_spread +
                      0.25 * w_div +
                      0.15 * w_ctx)

    return {
        "strength": strength,
        "spread": spread,
        "diversity": diversity,
        "avg_ayah_len": avg_ayah_len,
        "context_density": context_density,
        "concept_weight": concept_weight,
    }

# ---------------------------------------------------
# Smart Dome v3: القبة البصمية + الوزن المفهومي
# ---------------------------------------------------
def build_smart_dome_v3(root, colorscale):
    entry = get_root_entry(root)
    if not entry:
        return None

    metrics = compute_root_metrics(entry)
    strength = metrics["strength"]
    spread = metrics["spread"]
    diversity = metrics["diversity"]
    context_density = metrics["context_density"]
    concept_weight = metrics["concept_weight"]

    # تطبيع القيم
    s_norm = np.tanh(strength / 80.0)          # سلطان الحضور
    p_norm = np.tanh(spread / 20.0)            # مدى الانتشار
    d_norm = np.clip(diversity * 4.0, 0, 1)    # التنوع الدلالي
    c_norm = np.clip(context_density / 10.0, 0, 1)  # كثافة السياق
    w_norm = np.clip(concept_weight, 0, 1)     # الوزن المفهومي

    # عدد الأجنحة والتموجات (بصمة فريدة)
    k_wings = max(2, min(10, int(2 + p_norm * 8)))      # أجنحة الانتشار
    k_ripples = max(2, min(12, int(3 + d_norm * 9)))    # تموجات التنوع
    asym_factor = 0.3 * c_norm                          # لا تماثل من كثافة السياق

    # نصف قطر أساسي وارتفاع (يدخل فيها الوزن المفهومي)
    base_r = 0.6 + 0.3 * s_norm
    height_scale = 0.7 + 1.2 * w_norm   # الوزن المفهومي يرفع القبة

    # شبكة الزوايا
    theta = np.linspace(0, 2 * np.pi, 120)
    phi = np.linspace(0, np.pi / 2, 60)
    theta, phi = np.meshgrid(theta, phi)

    # معامل تموج إضافي من الوزن المفهومي
    weight_ripple = 0.25 + 0.35 * w_norm

    # معادلة البصمة الهندسية
    radial_mod = (
        1.0
        + weight_ripple * np.sin(k_wings * theta) * np.cos(k_ripples * phi)
        + asym_factor * np.sin(theta)
    )

    r = base_r * (1.0 + 0.4 * p_norm * np.sin(phi)) * radial_mod

    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = height_scale * r * np.cos(phi)

    surface = go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=z,  # اللون يتبع الارتفاع (الوزن المفهومي)
        colorscale=colorscale,
        showscale=False,
        opacity=0.96,
        hovertemplate=(
            f"الجذر: {root}<br>"
            "x: %{x:.2f}<br>"
            "y: %{y:.2f}<br>"
            "z: %{z:.2f}<extra></extra>"
        ),
        name=root,
    )

    fig = go.Figure(data=[surface])

    fig.update_layout(
        title=f"القبة البصمية المفهومية للجذر «{root}» — Smart Dome v3",
        scene=dict(
            xaxis=dict(
                title="محور الانتشار الأفقي",
                showgrid=True,
                zeroline=True,
                showbackground=True,
                backgroundcolor="rgba(245,245,245,0.7)",
            ),
            yaxis=dict(
                title="محور التنوع الجانبي",
                showgrid=True,
                zeroline=True,
                showbackground=True,
                backgroundcolor="rgba(245,245,245,0.7)",
            ),
            zaxis=dict(
                title="محور السلطان الرأسي / الوزن المفهومي",
                showgrid=True,
                zeroline=True,
                showbackground=True,
                backgroundcolor="rgba(245,245,245,0.7)",
            ),
        ),
        margin=dict(l=0, r=0, t=60, b=0),
    )

    return fig

# ---------------------------------------------------
# تدرجات لونية مميزة
# ---------------------------------------------------
# تدرج ذهبي للجذر الأول
GOLDEN_SCALE = [
    [0.0, "#4d3200"],   # بني داكن
    [0.3, "#806000"],   # ذهبي غامق
    [0.6, "#ffbf00"],   # ذهبي ساطع
    [1.0, "#ff4000"],   # برتقالي مائل للأحمر
]

# تدرج مميز مختلف للجذر الثاني (بارد/بنفسجي)
SECOND_SCALE = [
    [0.0, "#1b0033"],   # بنفسجي داكن
    [0.3, "#3f51b5"],   # أزرق بنفسجي
    [0.6, "#7c4dff"],   # بنفسجي ساطع
    [1.0, "#ff4081"],   # وردي قوي
]

# ---------------------------------------------------
# واجهة مِشكاة — Smart Dome v3
# ---------------------------------------------------
st.set_page_config(page_title="مِشكاة — Smart Dome v3", layout="wide")

st.title("🕌 مِشكاة — القبة البصمية المفهومية للجذور القرآنية (Smart Dome v3)")
st.write("كل جذر يُرسم هنا كبصمة هندسية مفهومية فريدة، وفق طيفه القرآني ووزنه المفهومي.")

tab_single, tab_compare = st.tabs(
    ["🔍 جذر واحد (Smart Dome v3)", "⚖️ مقارنة جذور (Smart Dome v3)"]
)

# ---------------------------------------------------
# TAB 1: جذر واحد
# ---------------------------------------------------
with tab_single:
    st.subheader("رصد بصمة جذر واحد")

    root_input = st.text_input("أدخل الجذر:", "كتب", key="single_root_input")

    entry = get_root_entry(root_input)
    if entry:
        metrics = compute_root_metrics(entry)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("قوة الحضور (عدد الآيات)", metrics["strength"])
        with c2:
            st.metric("انتشار الجذر (عدد السور)", metrics["spread"])
        with c3:
            st.metric("التنوع الدلالي", f"{metrics['diversity']:.3f}")

        c4, c5 = st.columns(2)
        with c4:
            st.metric("كثافة السياق", f"{metrics['context_density']:.3f}")
        with c5:
            st.metric("الوزن المفهومي الكلي", f"{metrics['concept_weight']:.3f}")

        fig_single = build_smart_dome_v3(root_input, colorscale=GOLDEN_SCALE)
        if fig_single:
            st.plotly_chart(fig_single, use_container_width=True, key="single_dome_v3")

        st.caption(
            "المحور الأفقي (x): مدى الانتشار عبر السور، "
            "المحور الجانبي (y): تنوع السياقات والكلمات المصاحبة، "
            "المحور الرأسي (z): سلطان الحضور والوزن المفهومي."
        )
    else:
        st.warning("لم يتم العثور على هذا الجذر في البيانات الحالية.")

# ---------------------------------------------------
# TAB 2: مقارنة جذور
# ---------------------------------------------------
with tab_compare:
    st.subheader("مقارنة البصمة الهندسية المفهومية بين جذرين")

    col1, col2 = st.columns(2)
    with col1:
        root1 = st.text_input("الجذر الأول:", "كتب", key="cmp_root1")
    with col2:
        root2 = st.text_input("الجذر الثاني:", "علم", key="cmp_root2")

    e1 = get_root_entry(root1)
    e2 = get_root_entry(root2)

    if e1 and e2:
        m1 = compute_root_metrics(e1)
        m2 = compute_root_metrics(e2)

        st.markdown("### 📊 ميزان المقاييس العددية والمفهومية")
        cA, cB = st.columns(2)
        with cA:
            st.markdown(f"#### {root1}")
            st.metric("قوة الحضور", m1["strength"])
            st.metric("انتشار الجذر", m1["spread"])
            st.metric("التنوع الدلالي", f"{m1['diversity']:.3f}")
            st.metric("الوزن المفهومي", f"{m1['concept_weight']:.3f}")
        with cB:
            st.markdown(f"#### {root2}")
            st.metric("قوة الحضور", m2["strength"])
            st.metric("انتشار الجذر", m2["spread"])
            st.metric("التنوع الدلالي", f"{m2['diversity']:.3f}")
            st.metric("الوزن المفهومي", f"{m2['concept_weight']:.3f}")

        fig_cmp = go.Figure()

        fig1 = build_smart_dome_v3(root1, colorscale=GOLDEN_SCALE)
        fig2 = build_smart_dome_v3(root2, colorscale=SECOND_SCALE)

        if fig1 and fig1.data:
            for tr in fig1.data:
                tr.name = root1
                fig_cmp.add_trace(tr)
        if fig2 and fig2.data:
            for tr in fig2.data:
                tr.name = root2
                fig_cmp.add_trace(tr)

        fig_cmp.update_layout(
            title=f"مقارنة القبتين البصميتين المفهومتين «{root1}» و «{root2}»",
            scene=dict(
                xaxis=dict(
                    title="محور الانتشار الأفقي",
                    showgrid=True,
                    zeroline=True,
                    showbackground=True,
                    backgroundcolor="rgba(245,245,245,0.7)",
                ),
                yaxis=dict(
                    title="محور التنوع الجانبي",
                    showgrid=True,
                    zeroline=True,
                    showbackground=True,
                    backgroundcolor="rgba(245,245,245,0.7)",
                ),
                zaxis=dict(
                    title="محور السلطان الرأسي / الوزن المفهومي",
                    showgrid=True,
                    zeroline=True,
                    showbackground=True,
                    backgroundcolor="rgba(245,245,245,0.7)",
                ),
            ),
            margin=dict(l=0, r=0, t=60, b=0),
        )

        st.plotly_chart(fig_cmp, use_container_width=True, key="compare_domes_v3")
        st.caption(
            "القبة الذهبية تمثل الجذر الأول، والقبة البنفسجية تمثل الجذر الثاني؛ "
            "راقب اختلاف الأجنحة والارتفاعات والتموجات لتقرأ الفوارق المفهومية بين الجذرين."
        )
    else:
        st.warning("تأكد أن كلا الجذرين موجودان في البيانات.")