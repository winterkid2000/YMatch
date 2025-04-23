from pydantic import BaseModel
from datetime import datetime
from typing import List

class RideRequestCreate(BaseModel):
    nickname: str
    departure: str
    destination: str
    departure_time: datetime

class RideRequestOut(RideRequestCreate):
    id: int
    class Config:
        orm_mode = True

class MatchProposalCreate(BaseModel):
    sender_nickname: str
    receiver_request_id: int
    proposed_time: str
    proposed_place: str

class MatchProposalOut(MatchProposalCreate):
    id: int
    status: str
    class Config:
        orm_mode = True
