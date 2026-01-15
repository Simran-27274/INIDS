from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level
from app.database import SessionLocal
from app.models.traffic import TrafficLog
from app.models.alert import Alert

DEMO_MODE=True
router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
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

    # 1️⃣ ML prediction
    prediction = predict(data)
    if DEMO_MODE and data.get("Destination Port") == 4444:
        prediction = "attack"

    # Ensure pure Python type (VERY IMPORTANT)
    if hasattr(prediction, "item"):
        prediction = prediction.item()

    # 2️⃣ Risk calculation
    risk = calculate_risk(prediction)
    severity = severity_level(risk)

    # 3️⃣ Save traffic log
    traffic = TrafficLog(
        protocol=str(data.get("protocol")),
        src_ip=data.get("src_ip", "unknown"),
        dst_ip=data.get("dst_ip", "unknown"),
        prediction=str(prediction)
    )
    db.add(traffic)
    db.commit()
    db.refresh(traffic)

    # 4️⃣ Create alert ONLY if risky
    if risk >= 50:
        alert = Alert(
            traffic_id=traffic.id,
            attack_type=str(prediction),
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