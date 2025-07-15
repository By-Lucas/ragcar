from sqlalchemy import Column, Integer, JSON, DateTime, Text

from sqlalchemy.sql import func

from app.db.base import Base


class CarModels(Base):
    __tablename__ = "car_models"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    filters_json = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
