from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/match", response_model=schemas.MatchProposalOut)
def create_match_proposal(proposal: schemas.MatchProposalCreate, db: Session = Depends(get_db)):
    db_proposal = models.MatchProposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

@router.get("/match/{receiver_id}", response_model=List[schemas.MatchProposalOut])
def get_proposals_for_receiver(receiver_id: int, db: Session = Depends(get_db)):
    return db.query(models.MatchProposal).filter(models.MatchProposal.receiver_request_id == receiver_id).all()

@router.get("/match/received/{nickname}", response_model=List[schemas.MatchProposalOut])
def get_received_proposals(nickname: str, db: Session = Depends(get_db)):
    ride_requests = db.query(models.RideRequest).filter(models.RideRequest.nickname == nickname).all()
    ids = [r.id for r in ride_requests]
    return db.query(models.MatchProposal).filter(models.MatchProposal.receiver_request_id.in_(ids)).all()
