# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_router import router as auth_router  # 수정된 경로
from app.api import ride, match
from app.views import home
from app.database import create_tables

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    # 배포시 프론트 주소를 여기에 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router, prefix="/auth")
app.include_router(ride.router)
app.include_router(match.router)
app.include_router(home.router)

create_tables()  # 앱 시작 시 DB 테이블 생성
