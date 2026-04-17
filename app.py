# ============================
#   Mishkat v12 — Conscious Unified System
#   Dynamic HSV Colors + Radial Layers Mode + Tooltip + Letter Cards
#   Root Engine v5.3 — Canonical Roots Only
#   Fusion Engine v2 + Conscious Map Engine
# ============================

import streamlit as st
import streamlit.components.v1 as components
import math
import colorsys
import json

from utils.data_loader import load_quran
from utils.root_engine import analyze_text_v5
from utils.root_canonizer import canonize_root
from utils.surah_map_engine import (
    get_surah_stats_v5,
    get_surah_signature_v5,
    get_surah_links_v5
)
from utils.gene_spectrum_engine import compute_gene_spectrum_v5
from utils.smart_dome_engine import build_smart_dome_v4
from utils.comparison_engine import compare_texts_v4
from utils.reasoning_engine import build_reasoning_path_v4
from utils.mesh_engine import build_mesh_networks_v3
from utils.letter_cards import get_letter_card
from utils.fusion_engine import run_full_analysis
from utils.conscious_map_engine import build_conscious_map

st.set_page_config(page_title="Mishkat v12", layout="wide")
st.title("🟣 Mishkat v12 — Conscious Unified System")
st.caption("تحليل دلالي | توجيه ذكي | آية مختارة | تفسير عميق | خريطة واعية")

@st.cache_data
def get_quran():
    return load_quran("data/quran.csv")

quran = get_quran()

# ============================================================
#   NORMALIZE QURAN KEYS
# ============================================================

normalized_quran = []
for a in quran:
    entry = {}
    if "surah" in a:
        entry["surah_number"] = int(a["surah"])
    elif "surah_number" in a:
        entry["surah_number"] = int(a["surah_number"])
    else:
        entry["surah_number"] = None

    if "ayah" in a:
        entry["ayah_number"] = int(a["ayah"])
    elif "ayah_number" in a:
        entry["ayah_number"] = int(a["ayah_number"])
    else:
        entry["ayah_number"] = None

    if "text" in a:
        entry["text"] = a["text"]
    elif "ayah_text" in a:
        entry["text"] = a["ayah_text"]
    else:
        entry["text"] = ""

    normalized_quran.append(entry)

quran = normalized_quran

# ============================================================
#   SURAH MAP v6 — DATA FIX LAYER
# ============================================================

def get_surah_text(quran, surah_number):
    return " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])

def get_surah_roots_canonical(quran, surah_number):
    """استخراج الجذور باستخدام Root Engine v5.3 مع التوحيد"""
    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v5(text)
    canonical_roots = []
    for root, count in analysis["root_frequency"]:
        canonical_root = canonize_root(root)
        if canonical_root and len(canonical_root) >= 3:
            canonical_roots.append((canonical_root, count))
    return canonical_roots

def get_surah_ayahs(quran, surah_number):
    return [
        {"ayah_number": a["ayah_number"], "text": a["text"]}
        for a in quran if a["surah_number"] == surah_number
    ]

def get_surah_structure(quran, surah_number):
    ayahs = get_surah_ayahs(quran, surah_number)
    roots = get_surah_roots_canonical(quran, surah_number)
    text = get_surah_text(quran, surah_number)
    return {
        "ayahs": ayahs,
        "root_frequency": roots,
        "text": text,
        "ayah_count": len(ayahs)
    }

# ============================================================
#   HEAVY FULL SEMANTIC CLASSIFIER
# ============================================================

def classify_root_semantic(root: str):
    r = root.strip()
    first = r[0] if len(r) > 0 else ""
    last = r[-1] if len(r) > 0 else ""
    semantic_score = 0

    if first in ["ق", "ط", "ظ"]:
        semantic_score += 3
    elif first in ["ع", "غ", "خ"]:
        semantic_score += 2
    elif first in ["م", "ن", "ل", "ر"]:
        semantic_score += 1

    if len(r) == 3:
        semantic_score += 1
    elif len(r) == 4:
        semantic_score += 2
    elif len(r) >= 5:
        semantic_score += 3

    if last in ["م", "ن"]:
        semantic_score += 1
    if last in ["ء", "ح", "خ"]:
        semantic_score += 2

    if "ّ" in r:
        semantic_score += 2

    if first in ["ع", "ف", "د"]:
        category = "knowledge"
    elif first in ["ق", "ط", "ص"]:
        category = "power"
    elif first in ["خ", "ب", "غ"]:
        category = "creation"
    elif first in ["م", "ن", "ل"]:
        category = "emotion"
    elif first in ["ر", "س", "ح"]:
        category = "movement"
    else:
        category = "neutral"

    return category, semantic_score

# ============================================================
#   HSV COLOR GENERATOR
# ============================================================

def hsv_color_for_root(root: str, weight: int, t: float):
    category, score = classify_root_semantic(root)
    hue_map = {
        "knowledge": 220/360,
        "power": 0/360,
        "creation": 120/360,
        "emotion": 300/360,
        "movement": 180/360,
        "neutral": 30/360
    }
    h = hue_map.get(category, 30/360)
    s = min(1.0, 0.4 + (score * 0.1))
    v = 0.6 + 0.3 * math.sin(t/700 + weight*0.3)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

# ============================================================
#   RADIAL LAYERS ENGINE
# ============================================================

def assign_radial_layer(weight):
    if weight >= 10:
        return 1
    elif weight >= 6:
        return 2
    elif weight >= 3:
        return 3
    else:
        return 4

# ============================
#   MAIN TABS
# ============================

tabs = st.tabs([
    "🧠 الاستعلام الذكي",
    "🧬 تحليل الجذور",
    "🗺️ الخريطة الواعية",
    "🧬 Gene Spectrum v5",
    "🕋 Smart Dome v4",
    "⚖️ المقارنات v4",
    "🧭 الاستدلال v4",
    "🕸 Mesh Networks v3",
    "🗺️ Surah Map v6 (Radial Layers)"
])

# =========================================================
# 1) 🧠 الاستعلام الذكي — مع Fusion Engine v2
# =========================================================
with tabs[0]:
    st.subheader("🧠 الاستعلام الذكي — Conscious Search")

    q = st.text_area("اكتب سؤالك:", key="search_query")
    if st.button("بحث", key="search_btn"):
        if not q.strip():
            st.warning("⚠️ الرجاء كتابة سؤال")
        else:
            result = run_full_analysis(q, quran)

            # =========================
            # الجذور
            # =========================
            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            # =========================
            # الحالة
            # =========================
            st.markdown("### 🧠 الحالة")
            st.info(result["state"])

            # =========================
            # التوجيه
            # =========================
            st.markdown("### 🧭 التوجيه")
            st.success(result["guidance"])

            # =========================
            # المسار (Journey)
            # =========================
            st.markdown("### 🌌 المسار القرآني")
            for step in result["journey"]:
                st.markdown(f"**{step['stage']}** — سورة {step['surah']}:{step['ayah']}")
                st.write(step["text"])
                st.markdown("---")

            # =========================
            # الآيات
            # =========================
            st.markdown("### 📖 آيات مرتبطة")
            for m in result["matches"][:10]:
                st.markdown(f"**سورة {m['surah_number']}:{m['ayah_number']}**")
                st.write(m["text"])
                st.markdown("---")

            # =========================
            # التفسير
            # =========================
            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['ayah'][:150]}...")
                st.info(t["tafsir"])

            # =========================
            # الاستدلال
            # =========================
            st.markdown("### 🧭 الاستدلال")
            st.write(result["reasoning"])

# =========================================================
# 2) 🧬 تحليل الجذور
# =========================================================
with tabs[1]:
    st.subheader("🧬 تحليل الجذور")
    text = st.text_area("اكتب نصًا للتحليل:")
    if st.button("تحليل الجذور"):
        analysis = analyze_text_v5(text)
        
        st.markdown("### 🔤 الجذور المستخرجة")
        st.write(analysis["root_frequency"])
        
        st.markdown("### 🧩 بطاقات الحروف")
        all_letters = set()
        for root, count in analysis["root_frequency"]:
            for letter in root:
                all_letters.add(letter)
        
        for letter in sorted(all_letters):
            card = get_letter_card(letter)
            if card:
                st.markdown(f"#### 🔤 الحرف: {letter}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("عدد الجذور", card.get("عدد_الجذور", "—"))
                    st.metric("القيمة الوظيفية", card.get("القيمة_الوظيفية", "—"))
                with col2:
                    st.metric("المجال الغالب", card.get("المجال_الغالب", "—"))
                    st.metric("أعلى الجذور", card.get("أعلى_الجذور", "—")[:20] + "...")
                with col3:
                    st.metric("بداية", card.get("بداية", "—"))
                    st.metric("وسط", card.get("وسط", "—"))
                    st.metric("نهاية", card.get("نهاية", "—"))
                st.markdown("---")

# =========================================================
# 3) 🗺️ الخريطة الواعية — Conscious Map
# =========================================================
with tabs[2]:
    st.subheader("🗺️ الخريطة الواعية — Conscious Map")

    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="conscious_map")

    if st.button("بناء الخريطة", key="build_map_btn"):
        with st.spinner("جاري بناء الخريطة الواعية..."):
            result = build_conscious_map(surah_num, quran)

            # =========================
            # الجذور
            # =========================
            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            # =========================
            # الآيات المحورية
            # =========================
            st.markdown("### 📖 آيات محورية")
            for ay in result["key_ayahs"]:
                st.markdown(f"**سورة {ay['surah_number']}:{ay['ayah_number']}**")
                st.write(ay["text"])
                st.markdown("---")

            # =========================
            # التفسير
            # =========================
            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['text'][:150]}...")
                st.info(t["tafsir"])

            # =========================
            # الاستدلال
            # =========================
            st.markdown("### 🧭 مسار الفهم")
            st.write(result["reasoning"])

# =========================================================
# 4) 🧬 Gene Spectrum v5
# =========================================================
with tabs[3]:
    st.subheader("🧬 Gene Spectrum v5")
    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="gene_spectrum_v5")
    surah_text = " ".join([a["text"] for a in quran if a["surah_number"] == surah_num])
    spectrum = compute_gene_spectrum_v5(surah_text)
    st.write(spectrum)

# =========================================================
# 5) 🕋 Smart Dome v4
# =========================================================
with tabs[4]:
    st.subheader("🕋 Smart Dome v4")
    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="smart_dome_v4")
    dome = build_smart_dome_v4(quran, surah_num)
    st.write(dome)

# =========================================================
# 6) ⚖️ المقارنات v4
# =========================================================
with tabs[5]:
    st.subheader("⚖️ المقارنات")
    t1 = st.text_area("النص الأول:")
    t2 = st.text_area("النص الثاني:")
    if st.button("قارن"):
        comp = compare_texts_v4(t1, t2)
        st.write(comp)

# =========================================================
# 7) 🧭 الاستدلال v4
# =========================================================
with tabs[6]:
    st.subheader("🧭 الاستدلال")
    text = st.text_area("النص:")
    if st.button("استدل"):
        path = build_reasoning_path_v4(quran, text)
        st.write(path)

# =========================================================
# 8) 🕸 Mesh Networks v3
# =========================================================
with tabs[7]:
    st.subheader("🕸 Mesh Networks v3")
    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="mesh_v3")
    mesh = build_mesh_networks_v3(quran, surah_num)
    st.markdown("### 🧬 العقد (الجذور)")
    st.write(mesh["nodes"])
    st.markdown("### 🔗 الروابط (العلاقات)")
    st.write(mesh["links"])
    st.markdown("### 📊 إحصائيات الشبكة")
    st.write({"عدد الجذور": mesh["root_count"], "عدد الروابط": mesh["link_count"]})

# =========================================================
# 9) 🗺️ Surah Map v6 (Radial Layers)
# =========================================================
with tabs[8]:
    st.subheader("🗺️ Surah Map v6 — الخريطة الدائرية (Root Engine v5.3)")

    surah_number = st.number_input("اختر رقم السورة:", min_value=1, max_value=114, value=1, key="surah_map_v6_radial")

    currentSurahRoots = get_surah_roots_canonical(quran, surah_number)

    def build_roots_json(t):
        roots_list = []
        for r, c in currentSurahRoots:
            color = hsv_color_for_root(r, c, t)
            layer = assign_radial_layer(c)
            letters = [L for L in r]
            domains = []
            for L in letters:
                card = get_letter_card(L)
                if card:
                    domains.append(card.get("المجال_الغالب", "عام"))
                else:
                    domains.append("عام")
            roots_list.append({
                "root": r,
                "weight": c,
                "color": color,
                "layer": layer,
                "letters": "، ".join(letters),
                "domains": "، ".join(domains[:3])
            })
        return json.dumps(roots_list)

    if not currentSurahRoots:
        st.warning("⚠️ لم يتم العثور على جذور لهذه السورة")
    else:
        st.success(f"✅ {len(currentSurahRoots)} جذراً مستخرجاً من Root Engine v5.3")

        html_code = """
        <div style='padding:10px; color:#e5e7eb; background:#020617; position:relative;'>
            <h3>الخريطة الدائرية للجذور — Root Engine v5.3</h3>

            <div id="tooltip" 
                 style="position:absolute; 
                        background:#111; 
                        color:#fff; 
                        padding:6px 10px; 
                        border-radius:6px; 
                        font-size:13px; 
                        display:none; 
                        pointer-events:none;
                        z-index:1000;
                        border:1px solid #22c55e;">
            </div>

            <canvas id="surahRadialMap" width="700" height="700"
                    style="background:#05060a; border-radius:50%; display:block; margin:auto;"></canvas>

            <script>
                let t = 0;
                let currentRoots = [];

                function drawFrame() {
                    const canvas = document.getElementById('surahRadialMap');
                    const ctx = canvas.getContext('2d');
                    const W = canvas.width;
                    const H = canvas.height;
                    const CX = W / 2;
                    const CY = H / 2;
                    const baseRadius = 120;
                    const maxRadius = 280;

                    const roots = currentRoots;

                    if (!roots || roots.length === 0) return;

                    ctx.clearRect(0, 0, W, H);

                    const grd = ctx.createRadialGradient(CX, CY, 50, CX, CY, maxRadius);
                    grd.addColorStop(0, '#111827');
                    grd.addColorStop(1, '#020617');
                    ctx.fillStyle = grd;
                    ctx.beginPath();
                    ctx.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
                    ctx.fill();

                    const layers = [160, 200, 240, 280];
                    
                    const layerColors = {
                        1: 'rgba(255,0,0,0.10)',
                        2: 'rgba(255,165,0,0.08)',
                        3: 'rgba(0,255,255,0.06)',
                        4: 'rgba(255,255,255,0.04)'
                    };

                    layers.forEach((ring, idx) => {
                        ctx.fillStyle = layerColors[idx + 1];
                        ctx.beginPath();
                        ctx.arc(CX, CY, ring, 0, 2 * Math.PI);
                        ctx.fill();
                    });

                    layers.forEach(ring => {
                        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.arc(CX, CY, ring, 0, 2 * Math.PI);
                        ctx.stroke();
                    });

                    ctx.strokeStyle = '#22c55e';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath();
                    ctx.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
                    ctx.stroke();

                    const pulse = 8 * Math.sin(t / 800);
                    ctx.strokeStyle = 'rgba(34,197,94,0.4)';
                    ctx.beginPath();
                    ctx.arc(CX, CY, baseRadius + pulse, 0, 2 * Math.PI);
                    ctx.stroke();

                    roots.forEach((r, idx) => {
                        const angle = (2 * Math.PI * idx) / roots.length;

                        let layerBase = 0;
                        if (r.layer === 1) layerBase = 160;
                        else if (r.layer === 2) layerBase = 200;
                        else if (r.layer === 3) layerBase = 240;
                        else if (r.layer === 4) layerBase = 280;

                        const dynamicRadius = layerBase + 10 * Math.sin(t / 600 + r.weight);

                        const x = CX + dynamicRadius * Math.cos(angle);
                        const y = CY + dynamicRadius * Math.sin(angle);

                        if (r.weight <= 2) {
                            ctx.beginPath();
                            ctx.fillStyle = r.color + "55";
                            ctx.arc(x, y, 3, 0, Math.PI * 2);
                            ctx.fill();
                            return;
                        }

                        ctx.strokeStyle = r.color;
                        ctx.lineWidth = 0.8;
                        ctx.beginPath();
                        ctx.moveTo(CX, CY);
                        ctx.lineTo(x, y);
                        ctx.stroke();

                        const nodeRadius = 6 + r.weight * 1.5;
                        ctx.fillStyle = r.color;
                        ctx.beginPath();
                        ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
                        ctx.fill();

                        ctx.strokeStyle = r.color.replace("rgb", "rgba").replace(")", ",0.4)");
                        ctx.beginPath();
                        ctx.arc(x, y, nodeRadius + 4 * Math.sin(t / 700 + idx), 0, 2 * Math.PI);
                        ctx.stroke();

                        ctx.fillStyle = '#e5e7eb';
                        ctx.font = '12px sans-serif';
                        ctx.textAlign = x >= CX ? 'left' : 'right';
                        ctx.fillText(r.root, x + (x >= CX ? 8 : -8), y - 4);
                    });

                    ctx.fillStyle = '#a5b4fc';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('الخريطة الدائرية للجذور — Root Engine v5.3', CX, CY - 6);

                    t++;
                    requestAnimationFrame(drawFrame);
                }

                const canvas = document.getElementById('surahRadialMap');
                const tooltip = document.getElementById('tooltip');

                canvas.addEventListener('mousemove', function(e) {
                    const rect = canvas.getBoundingClientRect();
                    const mx = e.clientX - rect.left;
                    const my = e.clientY - rect.top;
                    const scaleX = canvas.width / rect.width;
                    const scaleY = canvas.height / rect.height;
                    const canvasX = mx * scaleX;
                    const canvasY = my * scaleY;
                    
                    const CX_local = canvas.width / 2;
                    const CY_local = canvas.height / 2;
                    const roots_local = currentRoots;
                    const t_local = t;

                    let found = null;

                    roots_local.forEach((r, idx) => {
                        const angle = (2 * Math.PI * idx) / roots_local.length;
                        let layerBase = 0;
                        if (r.layer === 1) layerBase = 160;
                        else if (r.layer === 2) layerBase = 200;
                        else if (r.layer === 3) layerBase = 240;
                        else if (r.layer === 4) layerBase = 280;
                        const dynamicRadius = layerBase + 10 * Math.sin(t_local / 600 + r.weight);
                        const x = CX_local + dynamicRadius * Math.cos(angle);
                        const y = CY_local + dynamicRadius * Math.sin(angle);
                        const dx = canvasX - x;
                        const dy = canvasY - y;
                        const threshold = r.weight <= 2 ? 12 : r.weight * 2 + 8;
                        if (Math.sqrt(dx*dx + dy*dy) < threshold) {
                            found = r;
                        }
                    });

                    if (found) {
                        tooltip.style.left = (e.clientX + 15) + "px";
                        tooltip.style.top = (e.clientY + 15) + "px";
                        tooltip.style.display = "block";
                        tooltip.innerHTML = '<b>' + found.root + '</b><br>' +
                                            'الوزن: ' + found.weight + '<br>' +
                                            'الطبقة: ' + found.layer + '<br>' +
                                            'الحروف: ' + found.letters + '<br>' +
                                            'المجالات: ' + found.domains;
                    } else {
                        tooltip.style.display = "none";
                    }
                });

                function updateRoots() {
                    currentRoots = JSON.parse('""" + build_roots_json(0) + """');
                }

                updateRoots();
                setInterval(updateRoots, 800);
                drawFrame();
            </script>
        </div>
        """

        components.html(html_code, height=800)

# ============================================================
#   FINAL COMPATIBILITY CHECK
# ============================================================

st.markdown("---")
st.markdown("### ✅ نظام Mishkat v12 جاهز للتشغيل")

try:
    _ = quran[0]["surah_number"]
    _ = quran[0]["ayah_number"]
    _ = quran[0]["text"]
    st.success("✔ مفاتيح القرآن موحدة")
except:
    st.error("❌ مشكلة في مفاتيح القرآن")

try:
    test_roots = get_surah_roots_canonical(quran, 1)
    if test_roots:
        st.success(f"✔ Root Engine v5.3 يعمل — {len(test_roots)} جذراً للسورة 1")
    else:
        st.warning("⚠️ Root Engine v5.3 لم يستخرج جذوراً")
except Exception as e:
    st.error(f"❌ خطأ في Root Engine: {e}")

try:
    c = hsv_color_for_root("علم", 3, 100)
    st.success("✔ HSV Colors تعمل")
except:
    st.error("❌ مشكلة في HSV Colors")

try:
    card = get_letter_card("ا")
    if card:
        st.success("✔ Letter Cards تعمل")
    else:
        st.warning("⚠️ Letter Cards: بعض الحروف غير متوفرة")
except Exception as e:
    st.error(f"❌ خطأ في Letter Cards: {e}")

try:
    from utils.fusion_engine import run_full_analysis
    st.success("✔ Fusion Engine متصل")
except:
    st.warning("⚠️ Fusion Engine غير متصل")

try:
    from utils.conscious_map_engine import build_conscious_map
    st.success("✔ Conscious Map Engine متصل")
except:
    st.warning("⚠️ Conscious Map Engine غير متصل")