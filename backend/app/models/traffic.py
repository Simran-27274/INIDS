from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    protocol = Column(String, nullable=False)
    src_ip = Column(String, nullable=False)
    dst_ip = Column(String, nullable=False)
    prediction = Column(String, nullable=False)