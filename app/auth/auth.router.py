# app/auth/auth_router.py
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth.security import hash_password, verify_password
from ..auth.jwt_handler import create_access_token
from ..auth.email_otp import generate_otp, verify_otp
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# 회원가입 HTML
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 로그인 HTML
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 실제 회원가입 API
@router.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    nickname: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    new_user = models.User(
        email=email,
        hashed_password=hash_password(password),
        nickname=nickname,
        user_id=email.split("@")[0]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/auth/login", status_code=303)

# 로그인 API
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("access_token", access_token, httponly=True)
    return response





