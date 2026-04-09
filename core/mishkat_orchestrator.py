from .mishkat_processor import extract_mishkat_root, calculate_q_index
from .mishkat_db import save_session
from .state_normalizer import normalize_state

class MishkatSystem:
    def __init__(self):
        self.version = "1.0.0"
        self.identity = "Mishkat Sovereign System"

    def process_input(self, text, title="مسار وجودي جديد"):
        """
        تنسيق عملية المعالجة: استخلاص، تقييس، ثم حفظ
        """
        # 1. تحليل النص واستخراج الجذر والطور
        analysis = extract_mishkat_root(text)
        
        # 2. حساب مؤشر الوعي
        q_val = calculate_q_index(analysis["root"])
        
        # 3. تقييس الحالة لنظام مشكاة
        state = normalize_state({
            "id": analysis["root"],
            "label": text,
            "semantic_phase": analysis["phase"],
            "q_index": q_val
        })
        
        # 4. الأرشفة السيادية في قاعدة البيانات
        save_session(title, text, analysis["phase"])
        
        return state

    def get_system_status(self):
        return {
            "status": "Active",
            "identity": self.identity,
            "version": self.version
        }
