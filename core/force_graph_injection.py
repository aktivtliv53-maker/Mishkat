import json
import streamlit as st
from streamlit.components.v1 import html

_FORCE_GRAPH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/3d-force-graph@1.73.2/dist/3d-force-graph.min.js"></script>
    <style>
        body {{ margin: 0; background-color: #050816; }}
        #graph {{ width: 100vw; height: 100vh; }}
    </style>
</head>
<body>
    <div id="graph"></div>
    <script>
        const gData = {data_json};
        try {{
            const Graph = ForceGraph3D()(document.getElementById('graph'))
                .graphData(gData)
                .nodeLabel('label')
                .nodeColor(node => node.semantic_phase === 'light' ? '#ffeb3b' : '#f44336')
                .backgroundColor('#050816');
        }} catch (err) {{
            document.body.innerHTML = "<div style='color:white; padding:20px;'>خطأ في تشغيل الرادار: " + err + "</div>";
        }}
    </script>
</body>
</html>
"""

def render_force_graph(graph_data):
    payload = {
        "nodes": graph_data.get("nodes", []),
        "links": graph_data.get("edges", [])
    }
    
    html(
        _FORCE_GRAPH_TEMPLATE.format(data_json=json.dumps(payload, ensure_ascii=False)),
        height=600,
    )
