# app/api/ride.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..auth.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 택시 요청 등록 (로그인 필요)
@router.post("/ride", response_model=schemas.RideRequestOut)
def create_ride(
    ride: schemas.RideRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_ride = models.RideRequest(
        user_id=current_user.id,
        departure=ride.departure,
        destination=ride.destination,
        departure_time=ride.departure_time
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

# 사용자별 요청 리스트 (본인 요청만)
@router.get("/ride", response_model=list[schemas.RideRequestOut])
def get_user_rides(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.RideRequest).filter(
        models.RideRequest.user_id == current_user.id
    ).all()

# 요청 취소
@router.delete("/ride/{ride_id}")
def delete_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ride = db.query(models.RideRequest).filter(
        models.RideRequest.id == ride_id,
        models.RideRequest.user_id == current_user.id
    ).first()

    if not ride:
        raise HTTPException(status_code=404, detail="해당 요청이 존재하지 않거나 권한이 없습니다.")

    db.delete(ride)
    db.commit()
    return {"message": "요청이 취소되었습니다."}

    ride.is_active = False
    db.commit()
    return {"message": "Ride request canceled and related match proposals updated."}
