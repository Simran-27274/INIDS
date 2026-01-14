from fastapi import APIRouter
from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

@router.post("/")
def predict_traffic(data: dict):
    """
    Accepts network traffic data
    Returns prediction, risk score, and severity
    """

    # 1️⃣ ML prediction
    prediction = predict(data)

    # 2️⃣ Risk calculation
    risk = calculate_risk(prediction)
    severity = severity_level(risk)

    # 3️⃣ Response
    return {
        "prediction": prediction,
        "risk": risk,
        "severity": severity
    }