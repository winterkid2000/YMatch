# app/auth/deps.py
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from .jwt_handler import decode_access_token
from .. import models, database

# 현재 로그인된 사용자 가져오기 (쿠키 기반)
def get_current_user(request: Request, db: Session = Depends(database.get_db)) -> models.User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

