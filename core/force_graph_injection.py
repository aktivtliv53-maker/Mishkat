import json
import streamlit as st
from streamlit.components.v1 import html

_FORCE_GRAPH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body {{ margin: 0; overflow: hidden; background: #050816; color: #eee; }}
    #graph {{ width: 100vw; height: 100vh; }}
    #searchBox {{
      position: absolute;
      top: 10px;
      left: 10px;
      z-index: 10;
      background: rgba(0,0,0,0.7);
      padding: 8px;
      border-radius: 6px;
      font-family: sans-serif;
      color: #eee;
    }}
    #searchBox input {{
      width: 160px;
      padding: 4px;
      border-radius: 4px;
      border: 1px solid #555;
      background: #111;
      color: #eee;
    }}
  </style>
</head>
<body>
<div id="searchBox">
  <div>🔍 ابحث عن جذر:</div>
  <input id="searchInput" placeholder="اكتب الجذر..." />
</div>
<div id="graph"></div>

<script src="https://unpkg.com/3d-force-graph"></script>
<script>
  const data = {data_json};

  const colorByPhase = (node) => {{
    if (!node.semantic_phase) return '#00bcd4';
    switch (node.semantic_phase) {{
      case 'light': return '#ffeb3b';
      case 'mercy': return '#8bc34a';
      case 'power': return '#f44336';
      case 'purification': return '#03a9f4';
      case 'knowledge': return '#9c27b0';
      default: return '#00bcd4';
    }}
  }};

  const elem = document.getElementById('graph');

  const Graph = ForceGraph3D()(elem)
    .graphData(data)
    .nodeLabel(node => node.label || node.id)
    .nodeAutoColorBy('group')
    .nodeColor(colorByPhase)
    .nodeOpacity(0.9)
    .nodeRelSize(6)
    .linkOpacity(0.4)
    .linkWidth(link => link.weight ? Math.max(1, Math.log(1 + link.weight)) : 1)
    .linkColor(() => 'rgba(255,255,255,0.4)')
    .backgroundColor('#050816')
    .onNodeClick(node => {{
      const distance = 80;
      const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

      Graph.cameraPosition(
        {{ x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }},
        node,
        1500
      );
    }});

  const searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('keyup', (e) => {{
    const q = e.target.value.trim();
    if (!q) return;
    const target = data.nodes.find(n => n.id === q || n.label === q);
    if (target) {{
      Graph.nodeColor(node => node === target ? '#ff5722' : colorByPhase(node));
      const distance = 80;
      const distRatio = 1 + distance / Math.hypot(target.x, target.y, target.z);
      Graph.cameraPosition(
        {{ x: target.x * distRatio, y: target.y * distRatio, z: target.z * distRatio }},
        target,
        1500
      );
    }}
  }});
</script>
</body>
</html>
"""

def render_force_graph(graph_data):
    if not isinstance(graph_data, dict):
        st.info("لا توجد بيانات شبكة صالحة.")
        return

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    payload = {
        "nodes": nodes,
        "links": edges,
    }

    html(
        _FORCE_GRAPH_TEMPLATE.format(
            data_json=json.dumps(payload, ensure_ascii=False)
        ),
        height=600,
        scrolling=False,
    )
