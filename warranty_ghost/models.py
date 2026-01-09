import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    ghost_email = Column(String, unique=True, index=True, nullable=False)

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, index=True)
    price = Column(Float)
    purchase_date = Column(DateTime)
    warranty_end = Column(DateTime)
    raw_body = Column(Text)
    owner_id = Column(Integer) # Foreign key to User, but not enforcing for MVP
