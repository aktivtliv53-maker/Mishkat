import numpy as np
import plotly.graph_objects as go

from root_strength import get_root_strength
from root_spread import get_root_spread
from root_semantic import get_root_semantic_diversity

# قيم مرجعية للتطبيع (يمكن تعديلها لاحقًا)
MAX_STRENGTH = 300   # أقصى عدد آيات متوقّع لجذر قوي
MAX_SPREAD   = 114   # عدد السور
MAX_DIVERSITY = 0.5  # تنوّع دلالي عالي تقريبًا

def normalize_value(value, max_value):
    if max_value <= 0:
        return 0.0
    v = value / max_value
    return max(0.0, min(1.0, v))

def build_root_spherical_mesh(root):
    # 1) حساب المقاييس الثلاثة
    strength = get_root_strength(root)
    spread_count, _ = get_root_spread(root)
    diversity_ratio, unique_words, total_words = get_root_semantic_diversity(root)

    # 2) تطبيع
    s_norm = normalize_value(strength, MAX_STRENGTH)
    p_norm = normalize_value(spread_count, MAX_SPREAD)
    d_norm = normalize_value(diversity_ratio, MAX_DIVERSITY)

    # 3) تحويلها إلى معاملات نصف قطر
    # نصف قطر أساسي
    base_r = 0.6
    # القوة ترفع القبة
    height_factor = 0.4 + 0.6 * s_norm
    # الانتشار يوسع القبة
    spread_factor = 0.4 + 0.6 * p_norm
    # التنوع يضيف تموّجًا
    diversity_factor = 0.2 + 0.8 * d_norm

    # 4) توليد شبكة نصف كرة (قبة)
    theta = np.linspace(0, 2 * np.pi, 60)
    phi = np.linspace(0, np.pi / 2, 30)  # نصف كرة (قبة)
    theta, phi = np.meshgrid(theta, phi)

    # نصف القطر يتغير حسب التنوع
    r = base_r + diversity_factor * np.sin(2 * phi) * np.cos(3 * theta)

    # تطبيق القوة والانتشار
    x = spread_factor * r * np.cos(theta) * np.sin(phi)
    y = spread_factor * r * np.sin(theta) * np.sin(phi)
    z = height_factor * r * np.cos(phi)

    surface = go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale="Viridis",
        showscale=False,
        opacity=0.9,
    )

    fig = go.Figure(data=[surface])

    fig.update_layout(
        title=f"القبة النورانية للجذر «{root}»",
        scene=dict(
            xaxis_title="انتشار الجذر عبر السور",
            yaxis_title="تنوّع دلالي / تموّج",
            zaxis_title="قوة الحضور (عدد الآيات)",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            zaxis=dict(showgrid=False, zeroline=False),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig, {
        "strength": strength,
        "spread_count": spread_count,
        "diversity_ratio": diversity_ratio,
        "unique_words": unique_words,
        "total_words": total_words,
    }

if __name__ == "__main__":
    root = "كتب"
    fig, meta = build_root_spherical_mesh(root)
    print("مقاييس الجذر:", meta)
    fig.show()