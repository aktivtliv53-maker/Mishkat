import json
import streamlit as st
from streamlit.components.v1 import html

_FORCE_GRAPH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <script src="https://unpkg.com/3d-force-graph"></script>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #050816;
        }
        #graph {
            width: 100%;
            height: 100%;
            position: absolute;
            inset: 0;
        }
    </style>
</head>
<body>
    <div id="graph"></div>

    <script>
        const gData = {data_json};

        const data = {
            nodes: gData.nodes,
            links: gData.edges || gData.links
        };

        function initGraph() {
            const elem = document.getElementById('graph');
            if (!elem) return;

            const Graph = ForceGraph3D()(elem)
                .graphData(data)
                .nodeLabel(node => node.label || node.id)
                .nodeAutoColorBy('semantic_phase')
                .nodeRelSize(6)
                .linkOpacity(0.4)
                .backgroundColor('#050816');

            // إعادة ضبط الكاميرا بعد التحميل
            setTimeout(() => {
                Graph.zoomToFit(400);
            }, 800);
        }

        // تأخير بسيط لضمان تحميل DOM
        setTimeout(initGraph, 200);
    </script>
</body>
</html>
"""

def render_force_graph(graph_data):
    data_str = json.dumps(graph_data, ensure_ascii=False)
    html(_FORCE_GRAPH_TEMPLATE.replace("{data_json}", data_str), height=650)
