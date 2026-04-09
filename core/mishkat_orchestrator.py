from .mishkat_processor import process_text
from .mishkat_db import save_session
from .state_normalizer import normalize_state

class MishkatSystem:
    def __init__(self):
        self.version = "1.0.0"
        self.identity = "Mishkat Sovereign System"

    def process_input(self, text, title="مسار وجودي جديد"):
        """
        المعالج السيادي الموحد:
        - تحليل النص
        - بناء شبكة الجذور
        - تقييس الحالة
        - حفظ الجلسة
        """
        # 1) تحليل النص عبر المعالج الكامل
        state = process_text(text)

        # 2) تقييس الحالة
        normalized = normalize_state(state)

        # 3) حفظ الجلسة
        save_session(title, text, state["semantic_phases"][0] if state["semantic_phases"] else "unknown")

        return normalized

    def get_system_status(self):
        return {
            "status": "Active",
            "identity": self.identity,
            "version": self.version
        }
