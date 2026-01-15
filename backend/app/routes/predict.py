from fastapi import APIRouter
from app.services.ml_services import predict
from app.services.risk_service import calculate_risk, severity_level
from app.schemas.predict_schema import TrafficInput

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

@router.post("/")
def predict_traffic(payload: TrafficInput):

    features = payload.data   # 👈 real features here

    prediction = predict(features)
    risk = calculate_risk(prediction)
    severity = severity_level(risk)

    return {
        "prediction": prediction,
        "risk": risk,
        "severity": severity
    }