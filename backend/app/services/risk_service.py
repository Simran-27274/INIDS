def calculate_risk(prediction):
    if prediction == "attack":
        return 85
    return 20

def severity_level(score):
    if score > 80:
        return "HIGH"
    elif score > 50:
        return "MEDIUM"
    return "LOW"