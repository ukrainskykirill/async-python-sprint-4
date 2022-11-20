from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.db.db import Base


class ShortUrl(Base):
    __tablename__ = 'short_URL'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    short_url = Column(String(100), unique=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
