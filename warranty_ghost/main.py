import os
from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas, parser
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warranty Ghost")

# Build an absolute path to the templates directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Displays the main dashboard with a list of all parsed receipts.
    """
    receipts = db.query(models.Receipt).order_by(models.Receipt.purchase_date.desc()).all()
    total_value = sum(r.price for r in receipts if r.price)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "receipts": receipts,
        "total_value": total_value,
        "receipt_count": len(receipts)
    })

@app.post("/hooks/inbound")
async def inbound_email_hook(
    subject: str = Form(""),
    html: str = Form(""),
    to: str = Form(""),
    db: Session = Depends(get_db)
):
    """
    Simulated webhook endpoint for inbound emails (e.g., from SendGrid/Mailgun).
    Parses the email and saves the receipt data.
    """
    # For MVP, we're not linking to a user, just parsing the email
    # ghost_email = to.split('@')[0]
    
    email_parser = parser.EmailParser(html_content=html)
    parsed_data = email_parser.parse()

    receipt = models.Receipt(
        vendor=parsed_data.get("vendor"),
        price=parsed_data.get("price"),
        purchase_date=parsed_data.get("purchase_date"),
        warranty_end=parsed_data.get("warranty_end"),
        raw_body=parsed_data.get("raw_body"),
        # owner_id would be looked up from 'to' address in a real app
    )
    
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    
    return {"status": "success", "receipt_id": receipt.id}
