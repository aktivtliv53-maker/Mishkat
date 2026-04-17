import streamlit as st
import math
from core.mishkat_processor import get_root_data, build_root_network as build_neighbor_graph
from core.force_graph_injection import render_force_graph


def get_node_color(freq, is_core=False):
    if is_core:
        return "#FF4B4B"
    if freq > 100:
        return "#0033cc"
    if freq > 50:
        return "#1f77b4"
    if freq > 20:
        return "#4da6ff"
    return "#a0c4ff"


def get_node_size(freq, is_core=False):
    if is_core:
        return 50
    if freq == 0:
        return 5
    return 8 + math.log1p(freq) * 5


def render_visualizer():
    st.title("📡 رادار البصيرة القرآنية — Mishkat v1.6")

    search_query = st.text_input("أدخل الكلمة المراد تتبع جذرها قرآنياً:", "رحمة")

    if st.button("استنطاق الجذور"):
        results = get_root_data(search_query)

        if results and results.get('ayah_count', 0) > 0:
            st.success(f"الجذر: ({results['root']}) — {results['ayah_count']} آية — المعنى: {results.get('meanings', '—')}")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("🕸️ شبكة التلازم الجذري")
                nodes, edges = build_neighbor_graph(search_query)

                enhanced_nodes = []
                root_id = results['root']
                for node in nodes:
                    is_core = node["id"] == root_id
                    freq = node.get("freq", 0)
                    enhanced_nodes.append({
                        "id": node["id"],
                        "label": node["label"],
                        "semantic_phase": node.get("semantic_phase", "neighbor"),
                        "freq": freq,
                        "size": get_node_size(freq, is_core),
                        "color": get_node_color(freq, is_core),
                    })

                enhanced_edges = []
                for edge in edges:
                    enhanced_edges.append({
                        "source": edge["source"],
                        "target": edge["target"],
                        "weight": edge["weight"],
                    })

                graph_data = {"nodes": enhanced_nodes, "links": enhanced_edges}
                render_force_graph(graph_data)

            with col2:
                st.subheader("📖 كشاف الآيات")
                for v in results['ayahs']:
                    with st.expander(f"سورة {v['surah']} - آية {v['ayah_number']}"):
                        st.write(v['text'])
        else:
            st.error("لم يتم العثور على نتائج لهذا الجذر.")