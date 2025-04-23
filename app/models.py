from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

class RideRequest(Base):
    __tablename__ = "ride_requests"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    departure = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)

class MatchProposal(Base):
    __tablename__ = "match_proposals"
    id = Column(Integer, primary_key=True, index=True)
    sender_nickname = Column(String, nullable=False)
    receiver_request_id = Column(Integer, ForeignKey("ride_requests.id"), nullable=False)
    proposed_time = Column(String, nullable=False)
    proposed_place = Column(String, nullable=False)
    status = Column(String, default="pending")
