def detect_state(text):
    text = text.strip()

    if any(word in text for word in ["خائف", "قلق", "مرعوب"]):
        return "fear"

    if any(word in text for word in ["حزين", "مكتئب", "تعبان"]):
        return "sadness"

    if any(word in text for word in ["تبت", "أستغفر", "أريد التوبة"]):
        return "repentance"

    if any(word in text for word in ["رزق", "مال", "عمل"]):
        return "rizq"

    return "general"