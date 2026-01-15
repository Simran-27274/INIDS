from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.traffic import TrafficLog
from app.models.alert import Alert

router = APIRouter(
    prefix="/stats",
    tags=["Dashboard"]
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    """
    Dashboard statistics
    """

    total_traffic = db.query(func.count(TrafficLog.id)).scalar()
    total_alerts = db.query(func.count(Alert.id)).scalar()

    high = db.query(func.count(Alert.id)).filter(Alert.severity == "HIGH").scalar()
    medium = db.query(func.count(Alert.id)).filter(Alert.severity == "MEDIUM").scalar()
    low = db.query(func.count(Alert.id)).filter(Alert.severity == "LOW").scalar()

    return {
        "total_traffic": total_traffic or 0,
        "total_alerts": total_alerts or 0,
        "severity_breakdown": {
            "HIGH": high or 0,
            "MEDIUM": medium or 0,
            "LOW": low or 0
        }
    }