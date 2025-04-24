# app/auth/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from .security import hash_password, verify_password
from .jwt_handler import create_access_token
from .email_otp import generate_otp, send_otp_email, store_otp, verify_otp
from pydantic import EmailStr

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 회원가입
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not user.email.endswith("@yonsei.ac.kr") and not user.email.endswith("@mirae.yonsei.ac.kr"):
        raise HTTPException(status_code=400, detail="연세대학교 이메일만 사용 가능합니다.")

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user_id = user.email.split("@")[0]
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        user_id=user_id,
        nickname=user.nickname,
        hashed_password=hashed_pw,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 로그인
@router.post("/login", response_model=schemas.Token)
def login_user(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="이메일 인증이 완료되지 않았습니다.")

    token = create_access_token({"sub": user.user_id})
    return {"access_token": token, "token_type": "bearer"}

# OTP 요청
@router.post("/request-otp")
def request_otp(email_data: schemas.EmailRequest, db: Session = Depends(get_db)):
    code = generate_otp()
    send_otp_email(email_data.email, code)
    store_otp(db, email_data.email, code)
    return {"message": "인증 코드가 이메일로 전송되었습니다."}

# OTP 검증
@router.post("/verify-otp")
def verify_otp_code(email_data: schemas.EmailRequest, code: str, db: Session = Depends(get_db)):
    success = verify_otp(db, email_data.email, code)
    if not success:
        raise HTTPException(status_code=400, detail="인증 코드가 잘못되었거나 만료되었습니다.")
    return {"message": "이메일 인증이 완료되었습니다."}



