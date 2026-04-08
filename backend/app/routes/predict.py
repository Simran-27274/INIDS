from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level
from app.database import SessionLocal
from app.models.traffic import TrafficLog
from app.models.alert import Alert

DEMO_MODE = True
router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def predict_traffic(data: dict, db: Session = Depends(get_db)):
    """
    Predict traffic and auto-generate alerts
    """
    # 0️⃣ Map frontend keys to ML feature names if necessary
    # Example: 'dst_port' -> 'Destination Port'
    mapping = {
        "dst_port": "Destination Port",
        "flow_duration": "Flow Duration",
        "packet_size": "Average Packet Size",
        "protocol": "Protocol" # Not in FEATURE_ORDER but good to keep
    }
    
    ml_input = {}
    for k, v in data.items():
        ml_key = mapping.get(k, k)
        ml_input[ml_key] = v

    # 1️⃣ ML prediction
    if DEMO_MODE:
        # ✅ Force HIGH alert for testing
        prediction = 1  # 1 for attack
        risk = 90
        severity = "HIGH"
    else:
        prediction = predict(ml_input)
        # 2️⃣ Risk calculation
        risk = calculate_risk(prediction)
        severity = severity_level(risk)

    # 3️⃣ Save traffic log
    traffic = TrafficLog(
        protocol=str(data.get("protocol", "unknown")),
        src_ip=data.get("src_ip", "unknown"),
        dst_ip=data.get("dst_ip", "unknown"),
        prediction=str(prediction)
    )
    db.add(traffic)
    db.commit()
    db.refresh(traffic)

    # 4️⃣ Create alert ALWAYS for demo mode OR risky traffic
    if DEMO_MODE or (isinstance(prediction, int) and prediction > 0) or (isinstance(prediction, str) and prediction.lower() == "attack") or risk >= 50:
        alert = Alert(
            traffic_id=traffic.id,
            attack_type="Attack Detected" if str(prediction) == "1" else str(prediction),
            risk_score=float(risk),
            severity=severity
        )
        db.add(alert)
        db.commit()

    # 5️⃣ Response
    return {
        "traffic_id": traffic.id,
        "prediction": prediction,
        "risk": risk,
        "severity": severity
    }