from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from .database import Base
from datetime import datetime

# 사용자 모델 (연세메일 인증 기반)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)  # 연세메일 앞부분
    email = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# 기존 nickname 기반 요청 → user_id 외래키 연결
class RideRequest(Base):
    __tablename__ = "ride_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    departure = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

# sender_nickname → sender_id 외래키로 변경
class MatchProposal(Base):
    __tablename__ = "match_proposals"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_request_id = Column(Integer, ForeignKey("ride_requests.id"), nullable=False)
    proposed_time = Column(String, nullable=False)
    proposed_place = Column(String, nullable=False)
    status = Column(String, default="pending")  # "pending", "accepted", "rejected", "canceled"
