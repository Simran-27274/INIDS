from fastapi import APIRouter
from app.database import SessionLocal
from app.models.alert import Alert
from app.models.traffic import TrafficLog

router = APIRouter(
    prefix="/stats",
    tags=["Dashboard"]
)

@router.get("/")
def get_stats():
    db = SessionLocal()

    total_traffic = db.query(TrafficLog).count()
    total_alerts = db.query(Alert).count()
    high_risk = db.query(Alert).filter(Alert.severity == "HIGH").count()

    db.close()

    return {
        "total_traffic": total_traffic,
        "total_alerts": total_alerts,
        "high_risk_alerts": high_risk
    }