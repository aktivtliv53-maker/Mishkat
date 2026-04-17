# utils/root_metrics.py

def analyze_root(root):
    """
    تحليل بسيط للجذر (Placeholder).
    الهدف: منع الأخطاء وإعطاء بنية قابلة للتطوير لاحقاً.
    """
    if not root:
        return {
            "root": None,
            "letters": [],
            "strength": 0,
            "notes": "لا يوجد جذر"
        }

    letters = list(root)

    return {
        "root": root,
        "letters": letters,
        "strength": len(letters),  # placeholder
        "notes": f"تحليل أولي للجذر {root}"
    }