# app/auth/jwt_handler.py
from datetime import datetime, timedelta
from jose import jwt, JWTError

# 보안을 위해 실제 운영 시에는 환경변수 또는 .env 파일로 관리하세요.
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 엑세스 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 엑세스 토큰 디코딩
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # {'sub': user_id, 'exp': ...} 형태
    except JWTError:
        return None

# 유효성 검증 (선택)
def verify_access_token(token: str):
    return decode_access_token(token)
