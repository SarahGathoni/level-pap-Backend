from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.models.session import Session
from app.models.course import Course
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse

router = APIRouter()


@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    course_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List sessions with optional filters"""
    query = db.query(Session)
    
    if course_id:
        query = query.filter(Session.course_id == course_id)
    
    if date_from:
        query = query.filter(Session.date >= date_from)
    
    if date_to:
        query = query.filter(Session.date <= date_to)
    
    sessions = query.offset(skip).limit(limit).all()
    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: UUID, db: Session = Depends(get_db)):
    """Get session details"""
    session = db.query(Session).filter(Session.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.get("/courses/{course_id}/sessions", response_model=List[SessionResponse])
async def get_course_sessions(
    course_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all sessions for a specific course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    sessions = db.query(Session).filter(Session.course_id == course_id).all()
    return sessions


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new session (admin only)"""
    # Verify course exists
    course = db.query(Course).filter(Course.id == session_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Use course trainer if session doesn't have one
    trainer_id = session_data.trainer_id or course.trainer_id
    
    session = Session(
        **session_data.dict(exclude={"trainer_id"}),
        trainer_id=trainer_id
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    session_data: SessionUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a session (admin only)"""
    session = db.query(Session).filter(Session.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    update_data = session_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_session(
    session_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Cancel a session (admin only)"""
    from app.core.enums import SessionStatus
    
    session = db.query(Session).filter(Session.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session.status = SessionStatus.CANCELLED
    db.commit()
    return None

