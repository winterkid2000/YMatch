from fastapi import APIRouter, Depends, HTTPException
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
    return db.query(models.RideRequest).filter(models.RideRequest.is_active == True).order_by(models.RideRequest.departure_time).all()

@router.delete("/ride/{ride_id}")
def delete_ride(ride_id: int, db: Session = Depends(get_db)):
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    # 관련된 모든 match proposal도 상태를 'canceled'로 변경
    proposals = db.query(models.MatchProposal).filter(models.MatchProposal.receiver_request_id == ride_id).all()
    for proposal in proposals:
        proposal.status = "canceled"

    ride.is_active = False
    db.commit()
    return {"message": "Ride request canceled and related match proposals updated."}
