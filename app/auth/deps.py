# app/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .jwt_handler import decode_access_token
from .. import models
from ..database import SessionLocal

# OAuth2 스킴 설정 (token URL은 login 경로)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 현재 로그인된 사용자 가져오기
def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 토큰입니다."
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
    finally:
        db.close()
