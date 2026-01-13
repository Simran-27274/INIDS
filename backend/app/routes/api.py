from fastapi import APIRouter

router = APIRouter()

# Dummy /predict endpoint
@router.post("/predict")
def predict(data: dict):
    return {"prediction": "safe", "input_received": data}

# Dummy /alerts endpoint
@router.get("/alerts")
def alerts():
    return [
        {"id": 1, "attack_type": "DDoS", "severity": "HIGH"},
        {"id": 2, "attack_type": "Port Scan", "severity": "MEDIUM"}
    ]

# Dummy /stats endpoint
@router.get("/stats")
def stats():
    return {
        "total_alerts": 2,
        "high_risk": 1,
        "recent_activity": "2026-01-13 15:00"
    }