from fastapi import APIRouter, Depends, HTTPException
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
    return db.query(models.MatchProposal).filter(
        models.MatchProposal.receiver_request_id == receiver_id,
        models.MatchProposal.status != "canceled"
    ).all()

@router.get("/match/received/{nickname}", response_model=List[schemas.MatchProposalOut])
def get_received_proposals(nickname: str, db: Session = Depends(get_db)):
    ride_requests = db.query(models.RideRequest).filter(models.RideRequest.nickname == nickname).all()
    ids = [r.id for r in ride_requests]
    return db.query(models.MatchProposal).filter(
        models.MatchProposal.receiver_request_id.in_(ids),
        models.MatchProposal.status != "canceled"
    ).all()

@router.patch("/match/{proposal_id}")
def accept_proposal(proposal_id: int, db: Session = Depends(get_db)):
    proposal = db.query(models.MatchProposal).filter(models.MatchProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.status = "accepted"

    ride = db.query(models.RideRequest).filter(models.RideRequest.id == proposal.receiver_request_id).first()
    if ride:
        ride.is_active = False

    db.commit()
    return {"message": "Proposal accepted and ride request closed."}

@router.delete("/match/{proposal_id}")
def cancel_proposal(proposal_id: int, db: Session = Depends(get_db)):
    proposal = db.query(models.MatchProposal).filter(models.MatchProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.status = "canceled"
    db.commit()
    return {"message": "Match proposal canceled."}
