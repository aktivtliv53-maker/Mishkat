import numpy as np
import plotly.graph_objects as go
from utils_root_metrics import compute_root_metrics, get_root_entry

GOLDEN_SCALE = [
    [0.0, "#4d3200"],
    [0.3, "#806000"],
    [0.6, "#ffbf00"],
    [1.0, "#ff4000"],
]

SECOND_SCALE = [
    [0.0, "#1b0033"],
    [0.3, "#3f51b5"],
    [0.6, "#7c4dff"],
    [1.0, "#ff4081"],
]

def build_smart_dome_v3(root, colorscale):
    entry = get_root_entry(root)
    if not entry:
        return None

    m = compute_root_metrics(entry)

    s = np.tanh(m["strength"] / 80)
    p = np.tanh(m["spread"] / 20)
    d = min(1, m["diversity"] * 4)
    c = min(1, m["context_density"] / 10)
    w = m["concept_weight"]

    k_wings = max(2, int(2 + p * 8))
    k_ripples = max(2, int(3 + d * 9))
    asym = 0.3 * c

    base_r = 0.6 + 0.3 * s
    height = 0.7 + 1.2 * w

    theta = np.linspace(0, 2 * np.pi, 120)
    phi = np.linspace(0, np.pi / 2, 60)
    theta, phi = np.meshgrid(theta, phi)

    ripple = 0.25 + 0.35 * w

    radial = (
        1 +
        ripple * np.sin(k_wings * theta) * np.cos(k_ripples * phi) +
        asym * np.sin(theta)
    )

    r = base_r * (1 + 0.4 * p * np.sin(phi)) * radial

    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = height * r * np.cos(phi)

    fig = go.Figure(data=[
        go.Surface(
            x=x, y=y, z=z,
            surfacecolor=z,
            colorscale=colorscale,
            showscale=False,
            opacity=0.96,
            name=root,
        )
    ])

    fig.update_layout(
        title=f"Smart Dome v3 — «القبة البصمية المفهومية للجذر »{root}«",
        scene=dict(
            xaxis=dict(title="محور الانتشار"),
            yaxis=dict(title="محور التنوع"),
            zaxis=dict(title="محور السلطان / الوزن المفهومي"),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#0a0a1a",
        font=dict(color="white"),
    )

    return fig