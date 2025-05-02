# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Base, Purchase

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

class PurchaseRequest(BaseModel):
    email: str
    product_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/buy")
def buy_product(request: PurchaseRequest, db: Session = Depends(get_db)):
    new_purchase = Purchase(
        email=request.email,
        product_id=request.product_id
    )
    db.add(new_purchase)
    db.commit()
    return {"message": "Purchase logged"}
