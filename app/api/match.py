# app/api/match.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..auth.deps import get_current_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 합승 제안 생성 (로그인 필요)
@router.post("/match", response_model=schemas.MatchProposalOut)
def create_match_proposal(proposal: schemas.MatchProposalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_proposal = models.MatchProposal(
        sender_id=current_user.id,
        receiver_request_id=proposal.receiver_request_id,
        proposed_time=proposal.proposed_time,
        proposed_place=proposal.proposed_place
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

# 내가 받은 제안 조회
@router.get("/match/received", response_model=List[schemas.MatchProposalOut])
def get_received_proposals(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    my_requests = db.query(models.RideRequest).filter(models.RideRequest.user_id == current_user.id).all()
    ids = [r.id for r in my_requests]
    return db.query(models.MatchProposal).filter(models.MatchProposal.receiver_request_id.in_(ids), models.MatchProposal.status != "canceled").all()

# 내가 보낸 제안 조회
@router.get("/match/sent", response_model=List[schemas.MatchProposalOut])
def get_sent_proposals(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.MatchProposal).filter(models.MatchProposal.sender_id == current_user.id).all()

# 제안 수락 (POST 방식 허용)
@router.post("/match/{proposal_id}/accept")
def accept_proposal(proposal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    proposal = db.query(models.MatchProposal).filter(models.MatchProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="제안이 존재하지 않습니다.")
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == proposal.receiver_request_id).first()
    if ride.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="수락 권한이 없습니다.")

    proposal.status = "accepted"
    ride.is_active = False
    db.commit()
    return {"message": "제안을 수락했습니다."}

# 제안 거절 (POST 방식 허용)
@router.post("/match/{proposal_id}/reject")
def reject_proposal(proposal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    proposal = db.query(models.MatchProposal).filter(models.MatchProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="제안이 존재하지 않습니다.")
    ride = db.query(models.RideRequest).filter(models.RideRequest.id == proposal.receiver_request_id).first()
    if ride.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="거절 권한이 없습니다.")

    proposal.status = "rejected"
    db.commit()
    return {"message": "제안을 거절했습니다."}

# 제안 취소
@router.delete("/match/{proposal_id}")
def cancel_proposal(proposal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    proposal = db.query(models.MatchProposal).filter(models.MatchProposal.id == proposal_id).first()
    if not proposal or proposal.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="취소 권한이 없습니다.")
    proposal.status = "canceled"
    db.commit()
    return {"message": "제안을 취소했습니다."}


