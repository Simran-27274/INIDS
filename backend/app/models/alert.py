from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    traffic_id = Column(Integer, ForeignKey("traffic_logs.id"), nullable=False)
    attack_type = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)