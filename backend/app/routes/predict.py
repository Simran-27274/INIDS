from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level
from app.database_dep import get_db
from app.models.traffic import TrafficLog
from app.models.alert import Alert

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

@router.post("/")
def predict_traffic(data: dict, db: Session = Depends(get_db)):
    # 1️⃣ ML prediction
    raw_prediction = predict(data)
    prediction = "attack" if raw_prediction == 1 else "normal"


    # 2️⃣ Risk calculation
    risk = calculate_risk(raw_prediction)
    severity = severity_level(risk)

    # 3️⃣ Save traffic log
    traffic = TrafficLog(
        protocol=str(data.get("Destination Port","unknown")),
        src_ip="unknown",
        dst_ip="unknown",
        prediction=prediction
    )
    db.add(traffic)
    db.commit()
    db.refresh(traffic)

    # 4️⃣ If attack → create alert
    if prediction == "attack":
        alert = Alert(
            traffic_id=traffic.id,
            attack_type="ML Detected Attack",
            risk_score=risk,
            severity=severity
        )
        db.add(alert)
        db.commit()

    # 5️⃣ Response
    return {
        "prediction": prediction,
        "risk": risk,
        "severity": severity
    }