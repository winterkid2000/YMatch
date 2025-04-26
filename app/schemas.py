# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 회원가입 요청 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str

# 회원 응답 스키마
class UserOut(BaseModel):
    id: int
    user_id: str
    email: EmailStr
    nickname: str
    is_verified: bool

    class Config:
        orm_mode = True

# 로그인 요청 스키마
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 토큰 응답 스키마
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# OTP 요청 스키마
class EmailRequest(BaseModel):
    email: EmailStr

# RideRequest용 스키마 (예시 유지)
class RideRequestCreate(BaseModel):
    departure: str
    destination: str
    departure_time: datetime

class RideRequestOut(BaseModel):
    id: int
    departure: str
    destination: str
    departure_time: datetime
    is_active: bool

    class Config:
        orm_mode = True

# MatchProposal 스키마 (간단화 예시)
class MatchProposalCreate(BaseModel):
    receiver_request_id: int
    proposed_time: str
    proposed_place: str

class MatchProposalOut(BaseModel):
    id: int
    sender_id: int
    receiver_request_id: int
    proposed_time: str
    proposed_place: str
    status: str

    class Config:
        orm_mode = True
        
