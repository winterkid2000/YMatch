# app/views/home.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from ..auth.deps import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    rides = db.query(models.RideRequest).filter(models.RideRequest.is_active == True).all()
    my_rides = db.query(models.RideRequest).filter(models.RideRequest.user_id == current_user.id).all()
    my_ride_ids = [r.id for r in my_rides]
    received = db.query(models.MatchProposal).filter(models.MatchProposal.receiver_request_id.in_(my_ride_ids)).all()
    sent = db.query(models.MatchProposal).filter(models.MatchProposal.sender_id == current_user.id).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_user": current_user,
        "rides": rides,
        "received_matches": received,
        "sent_matches": sent
    })

# 로그아웃 라우터
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")  # 사용 중인 쿠키 이름에 따라 수정 필요
    return response
