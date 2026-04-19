# ============================
#   Mishkat v13 — Root Engine v6.6 Only
#   NO syllable splitting, NO preprocessing, NO semantic_engine
#   Final Sovereign Version
# ============================

import streamlit as st
import streamlit.components.v1 as components
import m# ============================
#   Mishkat v14 — Root Engine v7.0
#   Lexicon v7 — القرآن يفسر نفسه
#   السيادة الجذرية الكاملة
# ============================

import streamlit as st
import streamlit.components.v1 as components
import math
import colorsys
import json
import os
import sys
import pandas as pd

from utils.data_loader import load_quran
from utils.root_engine_v7 import analyze_text_v7
from utils.comparison_engine import compare_texts_v12
from utils.root_canonizer import canonize_root
from utils.gene_spectrum_engine import compute_gene_spectrum_v5
from utils.smart_dome_engine import build_smart_dome_v4
from utils.reasoning_engine import build_reasoning_path_v4
from utils.mesh_engine import build_mesh_networks_v3
from utils.letter_cards import get_letter_card
from utils.fusion_engine import run_full_analysis
from utils.conscious_map_engine import build_conscious_map

st.set_page_config(page_title="Mishkat v14", layout="wide")
st.title("🟣 Mishkat v14 — Root Engine v7.0")
st.caption("جذور قرآنية حقيقية | معجم معتمد | لا تجزئة | لا مقاطع صوتية")

# ============================
#   DATA LOADING
# ============================

def get_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def load_quran_data():
    try:
        path = get_path("data/quran.parquet")
        return pd.read_parquet(path)
    except:
        try:
            from utils.data_loader import load_quran as legacy_load
            return legacy_load()
        except:
            st.error("❌ لم يتم العثور على ملف القرآن")
            return []

quran = load_quran_data()

if isinstance(quran, pd.DataFrame):
    quran = quran.to_dict('records')

# ============================================================
#   NORMALIZE QURAN KEYS
# ============================================================

normalized_quran = []
for a in quran:
    entry = {}
    if "surah" in a:
        entry["surah_number"] = int(a["surah"]) if a["surah"] else 0
    elif "surah_number" in a:
        entry["surah_number"] = int(a["surah_number"]) if a["surah_number"] else 0
    else:
        entry["surah_number"] = 0

    if "ayah" in a:
        entry["ayah_number"] = int(a["ayah"]) if a["ayah"] else 0
    elif "ayah_number" in a:
        entry["ayah_number"] = int(a["ayah_number"]) if a["ayah_number"] else 0
    else:
        entry["ayah_number"] = 0

    if "text" in a:
        entry["text"] = a["text"]
    elif "ayah_text" in a:
        entry["text"] = a["ayah_text"]
    else:
        entry["text"] = ""

    normalized_quran.append(entry)

quran = normalized_quran

# ============================================================
#   SURAH MAP — ROOT ENGINE v7.0
# ============================================================

def get_surah_text(quran, surah_number):
    return " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])

def get_surah_roots_canonical(quran, surah_number):
    """مباشرة من Root Engine v7.0 - معتمد على Lexicon v7"""
    from utils.root_engine_v7 import analyze_text_v7
    from utils.root_canonizer import canonize_root

    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v7(text)

    canonical_roots = []
    for root, count in analysis["root_frequency"]:
        canonical_root = canonize_root(root)
        if canonical_root and len(canonical_root) >= 2:
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
    "⚖️ المقارنات v12",
    "🧭 الاستدلال v4",
    "🕸 Mesh Networks v3",
    "🗺️ Surah Map v7 (Radial Layers)"
])

# =========================================================
# 1) 🧠 الاستعلام الذكي
# =========================================================
with tabs[0]:
    st.subheader("🧠 الاستعلام الذكي — Conscious Search v7")

    q = st.text_area("اكتب سؤالك:", key="search_query")
    if st.button("بحث", key="search_btn"):
        if not q.strip():
            st.warning("⚠️ الرجاء كتابة سؤال")
        else:
            result = run_full_analysis(q, quran)

            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            st.markdown("### 🧠 الحالة")
            st.info(result["state"])

            st.markdown("### 🧭 التوجيه")
            st.success(result["guidance"])

            st.markdown("### 🌌 المسار القرآني")
            for step in result["journey"]:
                st.markdown(f"**{step['stage']}** — سورة {step['surah']}:{step['ayah']}")
                st.write(step["text"])
                st.markdown("---")

            st.markdown("### 📖 آيات مرتبطة")
            for m in result["matches"][:10]:
                st.markdown(f"**سورة {m['surah_number']}:{m['ayah_number']}**")
                st.write(m["text"])
                st.markdown("---")

            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['ayah'][:150]}...")
                st.info(t["tafsir"])

            st.markdown("### 🧭 الاستدلال")
            st.write(result["reasoning"])

# =========================================================
# 2) 🧬 تحليل الجذور — Root Engine v7.0
# =========================================================
with tabs[1]:
    st.subheader("🧬 تحليل الجذور — Root Engine v7.0")

    text = st.text_area("اكتب نصًا للتحليل:")
    if st.button("تحليل الجذور"):
        analysis = analyze_text_v7(text)
        
        st.markdown("### 🔤 الجذور المستخرجة (معتمدة من Lexicon v7)")
        st.write(analysis["root_frequency"])
        
        st.markdown("### 📊 أوزان الجذور")
        st.write(analysis.get("root_weights", {}))
        
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
# 3) 🗺️ الخريطة الواعية
# =========================================================
with tabs[2]:
    st.subheader("🗺️ الخريطة الواعية — Conscious Map v7")

    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="conscious_map")

    if st.button("بناء الخريطة", key="build_map_btn"):
        with st.spinner("جاري بناء الخريطة الواعية..."):
            result = build_conscious_map(surah_num, quran)

            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            st.markdown("### 📖 آيات محورية")
            for ay in result["key_ayahs"]:
                st.markdown(f"**سورة {ay['surah_number']}:{ay['ayah_number']}**")
                st.write(ay["text"])
                st.markdown("---")

            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['text'][:150]}...")
                st.info(t["tafsir"])

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
# 6) ⚖️ المقارنات v12
# =========================================================
with tabs[5]:
    st.subheader("⚖️ المقارنات — Comparison Engine v12")

    text1 = st.text_area("النص الأول:", key="compare_text1")
    text2 = st.text_area("النص الثاني:", key="compare_text2")

    if st.button("قارن", key="compare_btn"):
        if text1 and text2:
            result = compare_texts_v12(text1, text2)
            st.json(result)
        else:
            st.warning("⚠️ الرجاء إدخال النصين للمقارنة")

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
# 9) 🗺️ Surah Map v7 — الخريطة الدائرية (Root Engine v7.0)
# =========================================================
with tabs[8]:
    st.subheader("🗺️ Surah Map v7 — الخريطة الدائرية (Root Engine v7.0)")

    surah_number = st.number_input("اختر رقم السورة:", min_value=1, max_value=114, value=1, key="surah_map_v7")

    currentSurahRoots = get_surah_roots_canonical(quran, surah_number)

    def is_center_node(root):
        """تحديد العقدة المركزية (مثل منن أو مكرر الحروف)"""
        if root in ["منن", "مـنـن", "م ن ن"]:
            return True
        if len(root) == 3 and root[0] == root[1] == root[2]:
            return True
        return False

    def build_roots_json(t):
        roots_list = []
        seen = set()
        
        for r, c in currentSurahRoots:
            if r in seen:
                continue
            seen.add(r)
            
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
                "domains": "، ".join(domains[:3]),
                "isCenter": is_center_node(r)
            })
        return json.dumps(roots_list)

    if not currentSurahRoots:
        st.warning("⚠️ لم يتم العثور على جذور لهذه السورة")
    else:
        unique_roots = []
        seen_names = set()
        for r, c in currentSurahRoots:
            if r not in seen_names and not is_center_node(r):
                seen_names.add(r)
                unique_roots.append((r, c))
        
        st.success(f"✅ {len(unique_roots)} جذراً فريداً مستخرجاً من Root Engine v7.0 (معتمد من Lexicon v7)")

        html_code = """
        <div style="width:100%; display:flex; justify-content:center;">
          <div style="position:relative; width:100%; max-width:700px;">

            <canvas id="bgCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           background:#05060a; border-radius:50%; display:block;">
            </canvas>

            <canvas id="rootCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           position:absolute; top:0; left:0; pointer-events:auto;">
            </canvas>

            <div id="rootTooltip"
                 style="position:absolute; padding:6px 10px; background:rgba(15,23,42,0.95);
                        color:#e5e7eb; border-radius:6px; font-size:12px; pointer-events:none;
                        border:1px solid #4b5563; display:none; z-index:10;">
            </div>

          </div>
        </div>

        <script>
        (function () {

          const bgCanvas = document.getElementById('bgCanvas');
          const rootCanvas = document.getElementById('rootCanvas');
          const tooltip = document.getElementById('rootTooltip');

          function resize() {
            const size = bgCanvas.clientWidth;
            bgCanvas.width = size;
            bgCanvas.height = size;
            rootCanvas.width = size;
            rootCanvas.height = size;
          }
          resize();
          window.addEventListener('resize', resize);

          const bg = bgCanvas.getContext('2d');
          const ctx = rootCanvas.getContext('2d');

          let scale = 1;
          let offsetX = 0;
          let offsetY = 0;
          let isDragging = false;
          let lastX = 0;
          let lastY = 0;
          let lastTouchDistance = null;
          let hoverRoot = null;
          let baseRotation = 0;

          function drawBackground() {
            const W = bgCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;
            const maxRadius = W * 0.40;

            bg.clearRect(0, 0, W, W);

            const grd = bg.createRadialGradient(CX, CY, W * 0.05, CX, CY, maxRadius);
            grd.addColorStop(0, '#111827');
            grd.addColorStop(1, '#020617');
            bg.fillStyle = grd;
            bg.beginPath();
            bg.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
            bg.fill();

            bg.strokeStyle = '#22c55e';
            bg.lineWidth = W * 0.002;
            bg.beginPath();
            bg.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
            bg.stroke();

            bg.fillStyle = '#a5b4fc';
            bg.font = (W * 0.03) + 'px sans-serif';
            bg.textAlign = 'center';
            bg.fillText('الخريطة الدائرية للجذور — Root Engine v7.0', CX, CY - W * 0.02);
          }

          drawBackground();

          function getRoots() {
            const raw = window.surahRoots || [];
            return raw.map((r, i) => ({
              root: r.root,
              weight: r.weight,
              angle: (2 * Math.PI * i) / Math.max(1, raw.length),
              isCenter: r.isCenter || false
            }));
          }

          function screenToWorld(clientX, clientY) {
            const rect = rootCanvas.getBoundingClientRect();
            const x = (clientX - rect.left - offsetX) / scale;
            const y = (clientY - rect.top - offsetY) / scale;
            return { x, y };
          }

          function getRootAt(x, y, roots, CX, CY, baseRadius) {
            for (let i = 0; i < roots.length; i++) {
              const r = roots[i];
              if (r.isCenter) continue;
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25;
              const rx = CX + dynamicRadius * Math.cos(angle);
              const ry = CY + dynamicRadius * Math.sin(angle);
              const dist = Math.sqrt((x - rx)**2 + (y - ry)**2);
              if (dist < 20) return { r, rx, ry };
            }
            return null;
          }

          rootCanvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
          });

          rootCanvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
              offsetX += (e.clientX - lastX);
              offsetY += (e.clientY - lastY);
              lastX = e.clientX;
              lastY = e.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            } else {
              const { x, y } = screenToWorld(e.clientX, e.clientY);
              const W = rootCanvas.width;
              const CX = W / 2;
              const CY = W / 2;
              const baseRadius = W * 0.17;
              const roots = getRoots();
              const hit = getRootAt(x, y, roots, CX, CY, baseRadius);
              if (hit) {
                hoverRoot = hit;
                tooltip.style.display = 'block';
                tooltip.innerHTML = '<b>' + hit.r.root + '</b><br>الوزن: ' + hit.r.weight;
                tooltip.style.left = (e.clientX - rootCanvas.getBoundingClientRect().left + 10) + 'px';
                tooltip.style.top = (e.clientY - rootCanvas.getBoundingClientRect().top - 10) + 'px';
              } else {
                hoverRoot = null;
                tooltip.style.display = 'none';
              }
            }
          });

          rootCanvas.addEventListener('mouseup', () => isDragging = false);
          rootCanvas.addEventListener('mouseleave', () => isDragging = false);

          rootCanvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = -e.deltaY * 0.001;
            const oldScale = scale;
            scale += delta;
            scale = Math.max(0.4, Math.min(scale, 3));

            const rect = rootCanvas.getBoundingClientRect();
            const cx = e.clientX - rect.left;
            const cy = e.clientY - rect.top;

            offsetX = cx - (cx - offsetX) * (scale / oldScale);
            offsetY = cy - (cy - offsetY) * (scale / oldScale);
          }, { passive: false });

          rootCanvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
              isDragging = true;
              lastX = e.touches[0].clientX;
              lastY = e.touches[0].clientY;
            }
          });

          rootCanvas.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
              const t = e.touches[0];
              offsetX += (t.clientX - lastX);
              offsetY += (t.clientY - lastY);
              lastX = t.clientX;
              lastY = t.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            }
          });

          rootCanvas.addEventListener('touchend', () => isDragging = false);

          function drawRoots(t) {
            const W = rootCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;

            ctx.setTransform(scale, 0, 0, scale, offsetX, offsetY);
            ctx.clearRect(-offsetX/scale, -offsetY/scale, W/scale, W/scale);

            baseRotation += 0.0002;

            const roots = getRoots();

            roots.forEach((r, idx) => {
              if (r.isCenter) {
                return;
              }
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25 + 10 * Math.sin(t / 600 + idx);

              const x = CX + dynamicRadius * Math.cos(angle);
              const y = CY + dynamicRadius * Math.sin(angle);

              ctx.strokeStyle = 'rgba(96,165,250,0.5)';
              ctx.lineWidth = W * 0.0015;
              ctx.beginPath();
              ctx.moveTo(CX, CY);
              ctx.lineTo(x, y);
              ctx.stroke();

              const nodeRadius = (W * 0.008) + r.weight * (W * 0.002);

              if (hoverRoot && hoverRoot.r === r) {
                ctx.fillStyle = '#facc15';
              } else {
                ctx.fillStyle = '#f97316';
              }

              ctx.beginPath();
              ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
              ctx.fill();

              ctx.fillStyle = '#e5e7eb';
              ctx.font = (W * 0.02) + 'px sans-serif';
              ctx.textAlign = x >= CX ? 'left' : 'right';
              ctx.fillText(r.root, x + (x >= CX ? W * 0.015 : -W * 0.015), y - W * 0.01);
            });
          }

          function animate(t) {
            drawRoots(t || 0);
            requestAnimationFrame(animate);
          }

          function updateRoots() {
            window.surahRoots = JSON.parse('""" + build_roots_json(0) + """');
          }

          updateRoots();
          setInterval(updateRoots, 800);
          requestAnimationFrame(animate);
        })();
        </script>
        """

        st.components.v1.html(html_code, height=800)

# ============================================================
#   FINAL COMPATIBILITY CHECK
# ============================================================

st.markdown("---")
st.markdown("### ✅ نظام Mishkat v14 جاهز للتشغيل")

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
        unique = []
        seen = set()
        for r, c in test_roots:
            if r not in seen and not (len(r) == 3 and r[0] == r[1] == r[2]):
                seen.add(r)
                unique.append((r, c))
        st.success(f"✔ Root Engine v7.0 يعمل — {len(unique)} جذراً فريداً للسورة 1")
        st.write("عينة من الجذور:", [r for r, _ in unique[:15]])
    else:
        st.warning("⚠️ Root Engine v7.0 لم يستخرج جذوراً")
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
    st.warning("⚠️ Conscious Map Engine غير متصل")ath
import colorsys
import json
import os
import sys
import pandas as pd

from utils.data_loader import load_quran
from utils.root_engine import analyze_text_v6
from utils.comparison_engine import compare_texts_v12
from utils.root_canonizer import canonize_root
from utils.gene_spectrum_engine import compute_gene_spectrum_v5
from utils.smart_dome_engine import build_smart_dome_v4
from utils.reasoning_engine import build_reasoning_path_v4
from utils.mesh_engine import build_mesh_networks_v3
from utils.letter_cards import get_letter_card
from utils.fusion_engine import run_full_analysis
from utils.conscious_map_engine import build_conscious_map

st.set_page_config(page_title="Mishkat v13", layout="wide")
st.title("🟣 Mishkat v13 — Root Engine v6.6 Only")
st.caption("جذور حقيقية | لا تجزئة حروف | لا preprocessing | النسخة السيادية")

# ============================
#   DATA LOADING
# ============================

def get_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def load_quran_data():
    try:
        path = get_path("data/quran.parquet")
        return pd.read_parquet(path)
    except:
        try:
            from utils.data_loader import load_quran as legacy_load
            return legacy_load()
        except:
            st.error("❌ لم يتم العثور على ملف القرآن")
            return []

quran = load_quran_data()

if isinstance(quran, pd.DataFrame):
    quran = quran.to_dict('records')

# ============================================================
#   NORMALIZE QURAN KEYS
# ============================================================

normalized_quran = []
for a in quran:
    entry = {}
    if "surah" in a:
        entry["surah_number"] = int(a["surah"]) if a["surah"] else 0
    elif "surah_number" in a:
        entry["surah_number"] = int(a["surah_number"]) if a["surah_number"] else 0
    else:
        entry["surah_number"] = 0

    if "ayah" in a:
        entry["ayah_number"] = int(a["ayah"]) if a["ayah"] else 0
    elif "ayah_number" in a:
        entry["ayah_number"] = int(a["ayah_number"]) if a["ayah_number"] else 0
    else:
        entry["ayah_number"] = 0

    if "text" in a:
        entry["text"] = a["text"]
    elif "ayah_text" in a:
        entry["text"] = a["ayah_text"]
    else:
        entry["text"] = ""

    normalized_quran.append(entry)

quran = normalized_quran

# ============================================================
#   SURAH MAP — DIRECT ROOT ENGINE v6.6 (NO FALLBACK)
# ============================================================

def get_surah_text(quran, surah_number):
    return " ".join([a["text"] for a in quran if a["surah_number"] == surah_number])

def get_surah_roots_canonical(quran, surah_number):
    """مباشرة من Root Engine v6.6 - لا fallback، لا تجزئة"""
    from utils.root_engine import analyze_text_v6
    from utils.root_canonizer import canonize_root

    text = get_surah_text(quran, surah_number)
    analysis = analyze_text_v6(text)

    canonical_roots = []
    for root, count in analysis["root_frequency"]:
        canonical_root = canonize_root(root)
        if canonical_root and len(canonical_root) >= 2:
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
    "⚖️ المقارنات v12",
    "🧭 الاستدلال v4",
    "🕸 Mesh Networks v3",
    "🗺️ Surah Map v6 (Radial Layers)"
])

# =========================================================
# 1) 🧠 الاستعلام الذكي
# =========================================================
with tabs[0]:
    st.subheader("🧠 الاستعلام الذكي — Conscious Search")

    q = st.text_area("اكتب سؤالك:", key="search_query")
    if st.button("بحث", key="search_btn"):
        if not q.strip():
            st.warning("⚠️ الرجاء كتابة سؤال")
        else:
            result = run_full_analysis(q, quran)

            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            st.markdown("### 🧠 الحالة")
            st.info(result["state"])

            st.markdown("### 🧭 التوجيه")
            st.success(result["guidance"])

            st.markdown("### 🌌 المسار القرآني")
            for step in result["journey"]:
                st.markdown(f"**{step['stage']}** — سورة {step['surah']}:{step['ayah']}")
                st.write(step["text"])
                st.markdown("---")

            st.markdown("### 📖 آيات مرتبطة")
            for m in result["matches"][:10]:
                st.markdown(f"**سورة {m['surah_number']}:{m['ayah_number']}**")
                st.write(m["text"])
                st.markdown("---")

            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['ayah'][:150]}...")
                st.info(t["tafsir"])

            st.markdown("### 🧭 الاستدلال")
            st.write(result["reasoning"])

# =========================================================
# 2) 🧬 تحليل الجذور — Root Engine v6.6
# =========================================================
with tabs[1]:
    st.subheader("🧬 تحليل الجذور — Root Engine v6.6")

    text = st.text_area("اكتب نصًا للتحليل:")
    if st.button("تحليل الجذور"):
        analysis = analyze_text_v6(text)
        
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
# 3) 🗺️ الخريطة الواعية
# =========================================================
with tabs[2]:
    st.subheader("🗺️ الخريطة الواعية — Conscious Map")

    surah_num = st.number_input("اختر السورة:", min_value=1, max_value=114, value=1, key="conscious_map")

    if st.button("بناء الخريطة", key="build_map_btn"):
        with st.spinner("جاري بناء الخريطة الواعية..."):
            result = build_conscious_map(surah_num, quran)

            st.markdown("### 🧬 الجذور")
            st.write(result["roots"])

            st.markdown("### 📖 آيات محورية")
            for ay in result["key_ayahs"]:
                st.markdown(f"**سورة {ay['surah_number']}:{ay['ayah_number']}**")
                st.write(ay["text"])
                st.markdown("---")

            st.markdown("### 📘 التفسير")
            for t in result["tafsir"]:
                st.markdown(f"> {t['text'][:150]}...")
                st.info(t["tafsir"])

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
# 6) ⚖️ المقارنات v12
# =========================================================
with tabs[5]:
    st.subheader("⚖️ المقارنات — Comparison Engine v12")

    text1 = st.text_area("النص الأول:", key="compare_text1")
    text2 = st.text_area("النص الثاني:", key="compare_text2")

    if st.button("قارن", key="compare_btn"):
        if text1 and text2:
            result = compare_texts_v12(text1, text2)
            st.json(result)
        else:
            st.warning("⚠️ الرجاء إدخال النصين للمقارنة")

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
# 9) 🗺️ Surah Map v6 — الخريطة الدائرية (Root Engine v6.6)
#    النسخة السيادية النهائية
# =========================================================
with tabs[8]:
    st.subheader("🗺️ Surah Map v6 — الخريطة الدائرية (Root Engine v6.6)")

    surah_number = st.number_input("اختر رقم السورة:", min_value=1, max_value=114, value=1, key="surah_map_v6_radial")

    # الربط المباشر بـ get_surah_roots_canonical - لا fallback
    currentSurahRoots = get_surah_roots_canonical(quran, surah_number)

    def is_center_node(root):
        """تحديد العقدة المركزية (مثل منن أو مكرر الحروف)"""
        if root in ["منن", "مـنـن", "م ن ن"]:
            return True
        if len(root) == 3 and root[0] == root[1] == root[2]:
            return True
        return False

    def build_roots_json(t):
        """بناء JSON للجذور - مع منع التكرار والحفاظ على العقدة المركزية في JSON"""
        roots_list = []
        seen = set()
        
        for r, c in currentSurahRoots:
            # منع التكرار
            if r in seen:
                continue
            seen.add(r)
            
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
                "domains": "، ".join(domains[:3]),
                "isCenter": is_center_node(r)
            })
        return json.dumps(roots_list)

    if not currentSurahRoots:
        st.warning("⚠️ لم يتم العثور على جذور لهذه السورة")
    else:
        # إحصاء الجذور الفريدة (للعرض فقط، مع تجاهل العقدة المركزية)
        unique_roots = []
        seen_names = set()
        for r, c in currentSurahRoots:
            if r not in seen_names and not is_center_node(r):
                seen_names.add(r)
                unique_roots.append((r, c))
        
        st.success(f"✅ {len(unique_roots)} جذراً فريداً مستخرجاً من Root Engine v6.6")

        html_code = """
        <div style="width:100%; display:flex; justify-content:center;">
          <div style="position:relative; width:100%; max-width:700px;">

            <canvas id="bgCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           background:#05060a; border-radius:50%; display:block;">
            </canvas>

            <canvas id="rootCanvas"
                    style="width:100%; aspect-ratio:1/1;
                           position:absolute; top:0; left:0; pointer-events:auto;">
            </canvas>

            <div id="rootTooltip"
                 style="position:absolute; padding:6px 10px; background:rgba(15,23,42,0.95);
                        color:#e5e7eb; border-radius:6px; font-size:12px; pointer-events:none;
                        border:1px solid #4b5563; display:none; z-index:10;">
            </div>

          </div>
        </div>

        <script>
        (function () {

          const bgCanvas = document.getElementById('bgCanvas');
          const rootCanvas = document.getElementById('rootCanvas');
          const tooltip = document.getElementById('rootTooltip');

          function resize() {
            const size = bgCanvas.clientWidth;
            bgCanvas.width = size;
            bgCanvas.height = size;
            rootCanvas.width = size;
            rootCanvas.height = size;
          }
          resize();
          window.addEventListener('resize', resize);

          const bg = bgCanvas.getContext('2d');
          const ctx = rootCanvas.getContext('2d');

          let scale = 1;
          let offsetX = 0;
          let offsetY = 0;
          let isDragging = false;
          let lastX = 0;
          let lastY = 0;
          let lastTouchDistance = null;
          let hoverRoot = null;
          let baseRotation = 0;

          function drawBackground() {
            const W = bgCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;
            const maxRadius = W * 0.40;

            bg.clearRect(0, 0, W, W);

            const grd = bg.createRadialGradient(CX, CY, W * 0.05, CX, CY, maxRadius);
            grd.addColorStop(0, '#111827');
            grd.addColorStop(1, '#020617');
            bg.fillStyle = grd;
            bg.beginPath();
            bg.arc(CX, CY, maxRadius, 0, 2 * Math.PI);
            bg.fill();

            bg.strokeStyle = '#22c55e';
            bg.lineWidth = W * 0.002;
            bg.beginPath();
            bg.arc(CX, CY, baseRadius, 0, 2 * Math.PI);
            bg.stroke();

            bg.fillStyle = '#a5b4fc';
            bg.font = (W * 0.03) + 'px sans-serif';
            bg.textAlign = 'center';
            bg.fillText('الخريطة الدائرية للجذور — Root Engine v6.6', CX, CY - W * 0.02);
          }

          drawBackground();

          function getRoots() {
            const raw = window.surahRoots || [];
            return raw.map((r, i) => ({
              root: r.root,
              weight: r.weight,
              angle: (2 * Math.PI * i) / Math.max(1, raw.length),
              isCenter: r.isCenter || false
            }));
          }

          function screenToWorld(clientX, clientY) {
            const rect = rootCanvas.getBoundingClientRect();
            const x = (clientX - rect.left - offsetX) / scale;
            const y = (clientY - rect.top - offsetY) / scale;
            return { x, y };
          }

          function getRootAt(x, y, roots, CX, CY, baseRadius) {
            for (let i = 0; i < roots.length; i++) {
              const r = roots[i];
              // تجاهل العقدة المركزية في الـ hit detection
              if (r.isCenter) continue;
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25;
              const rx = CX + dynamicRadius * Math.cos(angle);
              const ry = CY + dynamicRadius * Math.sin(angle);
              const dist = Math.sqrt((x - rx)**2 + (y - ry)**2);
              if (dist < 20) return { r, rx, ry };
            }
            return null;
          }

          rootCanvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
          });

          rootCanvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
              offsetX += (e.clientX - lastX);
              offsetY += (e.clientY - lastY);
              lastX = e.clientX;
              lastY = e.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            } else {
              const { x, y } = screenToWorld(e.clientX, e.clientY);
              const W = rootCanvas.width;
              const CX = W / 2;
              const CY = W / 2;
              const baseRadius = W * 0.17;
              const roots = getRoots();
              const hit = getRootAt(x, y, roots, CX, CY, baseRadius);
              if (hit) {
                hoverRoot = hit;
                tooltip.style.display = 'block';
                tooltip.innerHTML = '<b>' + hit.r.root + '</b><br>الوزن: ' + hit.r.weight;
                tooltip.style.left = (e.clientX - rootCanvas.getBoundingClientRect().left + 10) + 'px';
                tooltip.style.top = (e.clientY - rootCanvas.getBoundingClientRect().top - 10) + 'px';
              } else {
                hoverRoot = null;
                tooltip.style.display = 'none';
              }
            }
          });

          rootCanvas.addEventListener('mouseup', () => isDragging = false);
          rootCanvas.addEventListener('mouseleave', () => isDragging = false);

          rootCanvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = -e.deltaY * 0.001;
            const oldScale = scale;
            scale += delta;
            scale = Math.max(0.4, Math.min(scale, 3));

            const rect = rootCanvas.getBoundingClientRect();
            const cx = e.clientX - rect.left;
            const cy = e.clientY - rect.top;

            offsetX = cx - (cx - offsetX) * (scale / oldScale);
            offsetY = cy - (cy - offsetY) * (scale / oldScale);
          }, { passive: false });

          rootCanvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
              isDragging = true;
              lastX = e.touches[0].clientX;
              lastY = e.touches[0].clientY;
            }
          });

          rootCanvas.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
              const t = e.touches[0];
              offsetX += (t.clientX - lastX);
              offsetY += (t.clientY - lastY);
              lastX = t.clientX;
              lastY = t.clientY;
              tooltip.style.display = 'none';
              hoverRoot = null;
            }
          });

          rootCanvas.addEventListener('touchend', () => isDragging = false);

          function drawRoots(t) {
            const W = rootCanvas.width;
            const CX = W / 2;
            const CY = W / 2;
            const baseRadius = W * 0.17;

            ctx.setTransform(scale, 0, 0, scale, offsetX, offsetY);
            ctx.clearRect(-offsetX/scale, -offsetY/scale, W/scale, W/scale);

            baseRotation += 0.0002;

            const roots = getRoots();

            roots.forEach((r, idx) => {
              // العقدة المركزية: لا ترسمها إطلاقاً (شفافة بالكامل)
              if (r.isCenter) {
                return;
              }
              
              const angle = r.angle + baseRotation;
              const dynamicRadius = baseRadius + 60 + r.weight * 25 + 10 * Math.sin(t / 600 + idx);

              const x = CX + dynamicRadius * Math.cos(angle);
              const y = CY + dynamicRadius * Math.sin(angle);

              ctx.strokeStyle = 'rgba(96,165,250,0.5)';
              ctx.lineWidth = W * 0.0015;
              ctx.beginPath();
              ctx.moveTo(CX, CY);
              ctx.lineTo(x, y);
              ctx.stroke();

              const nodeRadius = (W * 0.008) + r.weight * (W * 0.002);

              if (hoverRoot && hoverRoot.r === r) {
                ctx.fillStyle = '#facc15';
              } else {
                ctx.fillStyle = '#f97316';
              }

              ctx.beginPath();
              ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
              ctx.fill();

              ctx.fillStyle = '#e5e7eb';
              ctx.font = (W * 0.02) + 'px sans-serif';
              ctx.textAlign = x >= CX ? 'left' : 'right';
              ctx.fillText(r.root, x + (x >= CX ? W * 0.015 : -W * 0.015), y - W * 0.01);
            });
          }

          function animate(t) {
            drawRoots(t || 0);
            requestAnimationFrame(animate);
          }

          function updateRoots() {
            window.surahRoots = JSON.parse('""" + build_roots_json(0) + """');
          }

          updateRoots();
          setInterval(updateRoots, 800);
          requestAnimationFrame(animate);
        })();
        </script>
        """

        st.components.v1.html(html_code, height=800)

# ============================================================
#   FINAL COMPATIBILITY CHECK
# ============================================================

st.markdown("---")
st.markdown("### ✅ نظام Mishkat v13 جاهز للتشغيل")

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
        unique = []
        seen = set()
        for r, c in test_roots:
            if r not in seen and not (len(r) == 3 and r[0] == r[1] == r[2]):
                seen.add(r)
                unique.append((r, c))
        st.success(f"✔ Root Engine v6.6 يعمل — {len(unique)} جذراً فريداً للسورة 1")
        st.write("عينة من الجذور:", [r for r, _ in unique[:15]])
    else:
        st.warning("⚠️ Root Engine v6.6 لم يستخرج جذوراً")
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
