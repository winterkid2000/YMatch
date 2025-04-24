# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import auth_router
from .api import ride, match
from .views import home  # home 라우터 추가

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    # 여기에 실제 프론트 배포 주소 추가 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록 순서
app.include_router(auth_router.router, prefix="/auth")
app.include_router(ride.router)
app.include_router(match.router)
app.include_router(home.router)  # 루트 페이지 렌더링
