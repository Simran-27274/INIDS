from fastapi import APIRouter
from app.database import SessionLocal
from app.models.alert import Alert

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.get("/")
def get_alerts():
    db = SessionLocal()

    alerts = db.query(Alert).order_by(Alert.id.desc()).all()

    db.close()

    return alerts