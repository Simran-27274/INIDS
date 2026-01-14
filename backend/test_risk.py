from app.services.risk_service import calculate_risk, severity_level

prediction = "normal"

risk = calculate_risk(prediction)
severity = severity_level(risk)

print("prediction =", prediction)
print("risk =", risk)
print("severity =", severity)