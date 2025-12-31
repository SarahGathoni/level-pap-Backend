from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.models.corporate_request import CorporateRequest
from app.schemas.corporate_request import CorporateRequestCreate, CorporateRequestUpdate, CorporateRequestResponse

router = APIRouter()


@router.post("/requests", response_model=CorporateRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_corporate_request(
    request_data: CorporateRequestCreate,
    db: Session = Depends(get_db)
):
    """Submit a corporate training request (public endpoint)"""
    request = CorporateRequest(**request_data.dict())
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.get("/requests", response_model=List[CorporateRequestResponse])
async def list_corporate_requests(
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all corporate requests (admin only)"""
    query = db.query(CorporateRequest)
    
    if status_filter:
        from app.core.enums import CorporateRequestStatus
        try:
            status_enum = CorporateRequestStatus(status_filter)
            query = query.filter(CorporateRequest.status == status_enum)
        except ValueError:
            pass
    
    requests = query.order_by(CorporateRequest.created_at.desc()).offset(skip).limit(limit).all()
    return requests


@router.get("/requests/{request_id}", response_model=CorporateRequestResponse)
async def get_corporate_request(
    request_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get corporate request details (admin only)"""
    request = db.query(CorporateRequest).filter(CorporateRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate request not found"
        )
    
    return request


@router.put("/requests/{request_id}", response_model=CorporateRequestResponse)
async def update_corporate_request(
    request_id: UUID,
    request_data: CorporateRequestUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update corporate request status (admin only)"""
    request = db.query(CorporateRequest).filter(CorporateRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate request not found"
        )
    
    update_data = request_data.dict(exclude_unset=True)
    
    # Set responded_at and responded_by if status is being updated
    if "status" in update_data:
        request.responded_at = datetime.utcnow()
        request.responded_by = current_user.id
    
    for field, value in update_data.items():
        setattr(request, field, value)
    
    db.commit()
    db.refresh(request)
    return request


@router.delete("/requests/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_corporate_request(
    request_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a corporate request (admin only)"""
    request = db.query(CorporateRequest).filter(CorporateRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate request not found"
        )
    
    db.delete(request)
    db.commit()
    return None

