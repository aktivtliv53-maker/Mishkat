def generate_guidance(state):

    if state == "fear":
        return "أكثر من قول: حسبي الله ونعم الوكيل"

    if state == "sadness":
        return "اقرأ سورة الشرح وتأمل قوله: فإن مع العسر يسرا"

    if state == "repentance":
        return "ابدأ بالاستغفار 100 مرة، ثم اقرأ آيات التوبة"

    if state == "rizq":
        return "استغفر كثيراً، واقرأ سورة الواقعة"

    return "حافظ على الذكر والتوازن"