from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.models.trainer import Trainer
from app.schemas.trainer import TrainerCreate, TrainerUpdate, TrainerResponse

router = APIRouter()


@router.get("", response_model=List[TrainerResponse])
async def list_trainers(
    is_active: Optional[bool] = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all trainers"""
    query = db.query(Trainer)
    
    if is_active is not None:
        query = query.filter(Trainer.is_active == is_active)
    
    trainers = query.offset(skip).limit(limit).all()
    return trainers


@router.get("/{trainer_id}", response_model=TrainerResponse)
async def get_trainer(trainer_id: UUID, db: Session = Depends(get_db)):
    """Get trainer details"""
    trainer = db.query(Trainer).filter(
        Trainer.id == trainer_id,
        Trainer.is_active == True
    ).first()
    
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found"
        )
    
    return trainer


@router.post("", response_model=TrainerResponse, status_code=status.HTTP_201_CREATED)
async def create_trainer(
    trainer_data: TrainerCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new trainer (admin only)"""
    trainer = Trainer(**trainer_data.dict())
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    return trainer


@router.put("/{trainer_id}", response_model=TrainerResponse)
async def update_trainer(
    trainer_id: UUID,
    trainer_data: TrainerUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a trainer (admin only)"""
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found"
        )
    
    update_data = trainer_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trainer, field, value)
    
    db.commit()
    db.refresh(trainer)
    return trainer

