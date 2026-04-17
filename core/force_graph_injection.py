import json
import os
from streamlit.components.v1 import html

def render_force_graph(graph_data):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    with open(os.path.join(base, "3d-force-graph.min.js"), "r", encoding="utf-8") as f:
        js_graph = f.read()

    data_str = json.dumps(graph_data, ensure_ascii=False)

    template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <style>
        body {{ margin:0; overflow:hidden; background:#050816; }}
        #graph {{ width:100vw; height:600px; }}
    </style>
</head>
<body>
<div id="graph"></div>
<script>{js_graph}</script>
<script>
    const gData = {data_str};

    const Graph = ForceGraph3D()(document.getElementById('graph'))
        .graphData({{ nodes: gData.nodes, links: gData.links }})
        .nodeLabel(node => node.label + ' — ' + node.freq + ' آية')
        .nodeColor(node => node.color || '#00bcd4')
        .nodeVal(node => node.size || 6)
        .nodeRelSize(1)
        .linkWidth(link => link.weight ? Math.log1p(link.weight) * 1.5 : 1)
        .linkOpacity(0.6)
        .linkColor(() => 'rgba(255,255,255,0.4)')
        .backgroundColor('#050816')
        .nodeThreeObjectExtend(true)
        .nodeThreeObject(node => {{
            const THREE = Graph.renderer().info.render.constructor.name === 'WebGLRenderer'
                ? window.THREE || {{}} 
                : {{}};
            const canvas = document.createElement('canvas');
            canvas.width = 128; canvas.height = 32;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = node.color || '#00bcd4';
            ctx.font = 'bold 16px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.label, 64, 16);
            return canvas;
        }})
        .onNodeClick(node => {{
            const d = 80;
            const r = 1 + d / Math.hypot(node.x, node.y, node.z);
            Graph.cameraPosition({{x: node.x*r, y: node.y*r, z: node.z*r}}, node, 1000);
        }});

    let a = 0;
    setInterval(() => {{
        a += 0.003;
        Graph.cameraPosition({{x: 200*Math.sin(a), y: 40, z: 200*Math.cos(a)}});
    }}, 30);
    setTimeout(() => Graph.zoomToFit(400), 800);
</script>
</body>
</html>"""

    html(template, height=650, scrolling=False)