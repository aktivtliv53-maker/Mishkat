import json
import streamlit as st
from streamlit.components.v1 import html

_FORCE_GRAPH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/3d-force-graph"></script>
    <style>
        body { margin: 0; background-color: #050816; overflow: hidden; }
        #graph {
            width: 100vw;
            height: 100vh;
            position: absolute;
            top: 0;
            left: 0;
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

        // تأخير بسيط لضمان تحميل العنصر
        setTimeout(() => {
            const Graph = ForceGraph3D()(document.getElementById('graph'))
                .graphData(data)
                .nodeLabel('label')
                .nodeAutoColorBy('semantic_phase')
                .backgroundColor('#050816')
                .nodeRelSize(6)
                .linkOpacity(0.4);
        }, 200);
    </script>
</body>
</html>
"""

def render_force_graph(graph_data):
    data_str = json.dumps(graph_data, ensure_ascii=False)
    html(_FORCE_GRAPH_TEMPLATE.replace("{data_json}", data_str), height=700)
