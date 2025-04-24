import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models

OTP_EXPIRY_MINUTES = 5

# OTP 생성 함수
def generate_otp():
    return str(random.randint(100000, 999999))

# 메일 발송 함수 (Gmail SMTP 예시)
def send_otp_email(to_email: str, code: str):
    from_email = "your.email@gmail.com"  # 너의 Gmail 주소
    from_password = "your-app-password"  # Gmail 앱 비밀번호 사용

    msg = MIMEText(f"인증번호는 {code} 입니다. 5분 이내에 입력해주세요.")
    msg["Subject"] = "[YontakMatch] 이메일 인증코드"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, from_password)
        server.send_message(msg)

# DB에 OTP 저장 (User 모델 재사용)
def store_otp(db: Session, email: str, code: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        user.otp_code = code
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        db.commit()

# OTP 검증 후 인증 처리
def verify_otp(db: Session, email: str, code: str) -> bool:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and user.otp_code == code and user.otp_expiry and user.otp_expiry > datetime.utcnow():
        user.is_verified = True
        user.otp_code = None
        user.otp_expiry = None
        db.commit()
        return True
    return False

