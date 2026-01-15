from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.alert import Alert

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_alerts(db: Session = Depends(get_db)):
    """
    Fetch all alerts from DB
    """
    alerts = db.query(Alert).all()

    # Convert ORM objects to dict
    result = []
    for a in alerts:
        result.append({
            "id": a.id,
            "traffic_id": a.traffic_id,
            "attack_type": a.attack_type,
            "risk_score": a.risk_score,
            "severity": a.severity
        })

    return {"alerts": result}