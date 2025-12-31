from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.booking import Booking
from app.models.session import Session as SessionModel
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.core.enums import PaymentStatus

router = APIRouter()


@router.get("/users/{user_id}/bookings", response_model=List[BookingResponse])
async def get_user_bookings(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get bookings for a user (user can only see their own)"""
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these bookings"
        )
    
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get booking details"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Users can only view their own bookings
    if booking.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this booking"
        )
    
    return booking


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new booking"""
    # Check if session exists and is active
    session = db.query(SessionModel).filter(
        SessionModel.id == booking_data.session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check for duplicate booking
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.session_id == booking_data.session_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this session"
        )
    
    # Calculate seats left (only count paid bookings)
    paid_bookings = db.query(Booking).filter(
        Booking.session_id == booking_data.session_id,
        Booking.payment_status == PaymentStatus.PAID
    ).all()
    seats_booked = sum(b.seats for b in paid_bookings)
    seats_left = session.capacity - seats_booked
    
    if booking_data.seats > seats_left:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough seats available. Only {seats_left} seats left"
        )
    
    # Get course price
    from app.models.course import Course
    course = db.query(Course).filter(Course.id == session.course_id).first()
    price = course.price or 0
    total_amount = price * booking_data.seats
    
    booking = Booking(
        user_id=current_user.id,
        session_id=booking_data.session_id,
        seats=booking_data.seats,
        total_amount=total_amount,
        contact_phone=booking_data.contact_phone,
        special_requirements=booking_data.special_requirements,
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.put("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: UUID,
    cancellation_reason: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Users can only cancel their own bookings
    if booking.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking"
        )
    
    if booking.cancelled_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_reason = cancellation_reason
    booking.payment_status = PaymentStatus.REFUNDED
    
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/sessions/{session_id}/bookings", response_model=List[BookingResponse])
async def get_session_bookings(
    session_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all bookings for a session (admin only)"""
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    bookings = db.query(Booking).filter(Booking.session_id == session_id).all()
    return bookings

