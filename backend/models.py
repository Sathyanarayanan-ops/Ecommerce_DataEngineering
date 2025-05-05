from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    product_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    base_price = Column(Float)
    surge_price = Column(Float)
    
