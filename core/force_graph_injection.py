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
            links: gData.edges
        };

        function initGraph() {
            const elem = document.getElementById('graph');
            if (!elem) return;

            const Graph = ForceGraph3D()(elem)
                .graphData(data)
                .nodeLabel(node => `${node.label} — Q:${node.q_index}`)
                .nodeAutoColorBy('semantic_phase')
                .nodeRelSize(6)
                .linkOpacity(0.4)
                .backgroundColor('#050816');

            // حركة كاميرا سينمائية
            let angle = 0;
            setInterval(() => {
                angle += 0.003;
                Graph.cameraPosition({
                    x: 200 * Math.sin(angle),
                    y: 40,
                    z: 200 * Math.cos(angle)
                });
            }, 30);

            // تكبير تلقائي
            setTimeout(() => {
                Graph.zoomToFit(400);
            }, 800);
        }

        setTimeout(initGraph, 200);
    </script>
</body>
</html>
"""

def render_force_graph(graph_data):
    data_str = json.dumps(graph_data, ensure_ascii=False)
    html(_FORCE_GRAPH_TEMPLATE.replace("{data_json}", data_str), height=650)
