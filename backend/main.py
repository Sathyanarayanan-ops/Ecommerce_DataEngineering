
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from database import SessionLocal, engine
from models import Base, Purchase

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

class PurchaseRequest(BaseModel):
    email: str
    product_id: int

@app.on_event("startup")
def seed_base_prices():
    """Initialize base prices for all products on application startup"""
    db = SessionLocal()
    try:
        # Base prices matching Spark's price_df
        base_prices = [
            {"product_id": 1, "base_price": 3.99},
            {"product_id": 2, "base_price": 2.99},
            {"product_id": 3, "base_price": 4.99},
            {"product_id": 4, "base_price": 5.99},
            {"product_id": 5, "base_price": 2.99},
            {"product_id": 6, "base_price": 9.99},
            {"product_id": 7, "base_price": 19.99},
            {"product_id": 8, "base_price": 19.99},
            {"product_id": 9, "base_price": 6.99},
        ]
        
        for price_info in base_prices:
            # Check if product has any price entries
            exists = db.query(Purchase).filter(
                Purchase.product_id == price_info["product_id"],
                Purchase.base_price.isnot(None)
            ).first()
            
            if not exists:
                purchase = Purchase(
                    email="system@seed",
                    product_id=price_info["product_id"],
                    base_price=price_info["base_price"],
                    surge_price=price_info["base_price"],  # Initial surge = base
                    timestamp=datetime.utcnow()
                )
                db.add(purchase)
        
        db.commit()
    except Exception as e:
        print(f"Error seeding base prices: {str(e)}")
        db.rollback()
    finally:
        db.close()

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

# @app.get("/latest_prices")
# def get_latest_prices(db: Session = Depends(get_db)):
#     product_ids = db.query(Purchase.product_id).distinct().all()
#     result = []
#     print("\n=== DEBUG: Latest Prices Query ===")

#     for (product_id,) in product_ids:
#         latest = db.query(Purchase)\
#             .filter(Purchase.product_id == product_id)\
#             .filter(Purchase.base_price != None)\
#             .order_by(Purchase.timestamp.desc())\
#             .first()

#         print(f"Product {product_id}:")
#         if latest:
#             print(f"  Base: {latest.base_price} | Surge: {latest.surge_price} | Time: {latest.timestamp}")
#             result.append({
#                 "product_id": product_id,
#                 "base_price": latest.base_price,
#                 "surge_price": latest.surge_price
#             })
#     print("===\n")
#     return result

@app.get("/latest_prices")
def get_latest_prices(db: Session = Depends(get_db)):
    # Get all distinct products with any price history
    product_ids = db.query(Purchase.product_id).distinct().all()
    result = []
    
    for (product_id,) in product_ids:
        # Get the latest entry with BOTH prices populated
        latest = db.query(Purchase)\
            .filter(Purchase.product_id == product_id)\
            .filter(Purchase.base_price.isnot(None))\
            .filter(Purchase.surge_price.isnot(None))\
            .order_by(Purchase.timestamp.desc())\
            .first()

        if latest:
            result.append({
                "product_id": product_id,
                "base_price": latest.base_price,
                "surge_price": latest.surge_price
            })
    
    return result

