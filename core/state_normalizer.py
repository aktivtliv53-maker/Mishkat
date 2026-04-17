def normalize_state(raw_data):
    """تحويل البيانات الخام إلى تنسيق 'مشكاة' الموحد"""
    normalized = {
        "id": raw_data.get("id", "unknown"),
        "label": raw_data.get("label", ""),
        "semantic_phase": raw_data.get("semantic_phase", "light"),
        "q_index": raw_data.get("q_index", 0.0),
        "orbits": raw_data.get("orbits", [])
    }
    return normalized

def map_phase_to_color(phase):
    phases = {
        "light": "#ffeb3b",
        "power": "#f44336",
        "purification": "#03a9f4",
        "mercy": "#8bc34a",
        "knowledge": "#9c27b0"
    }
    return phases.get(phase, "#00bcd4")
