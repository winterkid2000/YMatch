from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ride", response_model=schemas.RideRequestOut)
def create_ride(request: schemas.RideRequestCreate, db: Session = Depends(get_db)):
    db_request = models.RideRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/ride", response_model=List[schemas.RideRequestOut])
def get_rides(db: Session = Depends(get_db)):
    return db.query(models.RideRequest).order_by(models.RideRequest.departure_time).all()
