from fastapi import APIRouter
from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level
from app.database import SessionLocal
from app.models.traffic import TrafficLog
from app.models.alert import Alert

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

@router.post("/")
def predict_traffic(data: dict):
    """
    Accepts network traffic data
    Returns prediction, risk score, severity
    Also stores traffic logs and alerts in DB
    """
    # 1️⃣ ML prediction
    prediction = predict(data)

    # 2️⃣ Risk calculation
    risk = calculate_risk(prediction)
    severity = severity_level(risk)

    # 3️⃣ Store in DB
    db = SessionLocal()
    
    # Create traffic log
    traffic_entry = TrafficLog(
        protocol=data.get("protocol"),
        src_ip=data.get("src_ip", "N/A"),
        dst_ip=data.get("dst_ip", "N/A"),
        prediction=prediction
    )
    db.add(traffic_entry)
    db.commit()
    db.refresh(traffic_entry)

    # Create alert if high risk
    if risk > 50:
        alert_entry = Alert(
            traffic_id=traffic_entry.id,
            attack_type=prediction,
            risk_score=risk,
            severity=severity
        )
        db.add(alert_entry)
        db.commit()

    db.close()

    # 4️⃣ Return response
    return {
        "prediction": prediction,
        "risk": risk,
        "severity": severity
    }