def calculate_risk(prediction):
    # Handle both string and numeric representations of an attack
    p = str(prediction).lower()
    if p in ["attack", "1"]:
        return 92
    return 15

def severity_level(score):
    if score > 80:
        return "HIGH"
    elif score > 50:
        return "MEDIUM"
    return "LOW"