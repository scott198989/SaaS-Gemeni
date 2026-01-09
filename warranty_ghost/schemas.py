from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReceiptBase(BaseModel):
    vendor: Optional[str] = None
    price: Optional[float] = None
    purchase_date: Optional[datetime] = None
    warranty_end: Optional[datetime] = None
    raw_body: Optional[str] = None

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    ghost_email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    receipts: list[Receipt] = []

    class Config:
        orm_mode = True
