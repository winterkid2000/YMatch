from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import datetime
from ..database import SessionLocal
from ..models import RideRequest

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# 홈페이지 - HTML 폼 표시
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 폼 제출 처리 - 택시 요청 등록
@router.post("/submit")
def submit_ride(
    request: Request,
    nickname: str = Form(...),
    departure: str = Form(...),
    destination: str = Form(...),
    departure_time: str = Form(...)
):
    db = SessionLocal()
    ride = RideRequest(
        nickname=nickname,
        departure=departure,
        destination=destination,
        departure_time=datetime.fromisoformat(departure_time)
    )
    db.add(ride)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)
