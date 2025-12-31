from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import secrets
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import PaymentInitiate, PaymentResponse
from app.core.enums import PaymentProvider, PaymentTransactionStatus, PaymentStatus

router = APIRouter()


@router.post("/mpesa/initiate", response_model=PaymentResponse)
async def initiate_mpesa_payment(
    payment_data: PaymentInitiate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Initiate M-Pesa payment"""
    if payment_data.provider != PaymentProvider.MPESA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid provider for this endpoint"
        )
    
    if not payment_data.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number required for M-Pesa"
        )
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to pay for this booking"
        )
    
    if booking.payment_status != PaymentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking payment status is not pending"
        )
    
    # Check if payment already exists
    existing_payment = db.query(Payment).filter(Payment.booking_id == payment_data.booking_id).first()
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already initiated for this booking"
        )
    
    # Generate payment reference
    payment_reference = f"MPESA_{secrets.token_hex(8).upper()}"
    
    # Create payment record
    payment = Payment(
        booking_id=payment_data.booking_id,
        provider=PaymentProvider.MPESA,
        payment_reference=payment_reference,
        amount=booking.total_amount,
        currency="KES",
        status=PaymentTransactionStatus.PENDING,
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    # TODO: Integrate with M-Pesa API
    # This is a placeholder - implement actual M-Pesa integration
    # from app.services.payments.mpesa import initiate_mpesa_stk_push
    # mpesa_response = initiate_mpesa_stk_push(
    #     phone=payment_data.phone,
    #     amount=float(booking.total_amount),
    #     reference=payment_reference
    # )
    # payment.provider_transaction_id = mpesa_response.get("CheckoutRequestID")
    # payment.provider_response = mpesa_response
    # db.commit()
    
    return payment


@router.post("/flutterwave/initiate", response_model=PaymentResponse)
async def initiate_flutterwave_payment(
    payment_data: PaymentInitiate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Initiate Flutterwave payment"""
    if payment_data.provider != PaymentProvider.FLUTTERWAVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid provider for this endpoint"
        )
    
    if not payment_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email required for Flutterwave"
        )
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to pay for this booking"
        )
    
    if booking.payment_status != PaymentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking payment status is not pending"
        )
    
    # Check if payment already exists
    existing_payment = db.query(Payment).filter(Payment.booking_id == payment_data.booking_id).first()
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already initiated for this booking"
        )
    
    # Generate payment reference
    payment_reference = f"FLW_{secrets.token_hex(8).upper()}"
    
    # Create payment record
    payment = Payment(
        booking_id=payment_data.booking_id,
        provider=PaymentProvider.FLUTTERWAVE,
        payment_reference=payment_reference,
        amount=booking.total_amount,
        currency="KES",
        status=PaymentTransactionStatus.PENDING,
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    # TODO: Integrate with Flutterwave API
    # This is a placeholder - implement actual Flutterwave integration
    
    return payment


@router.get("/status", response_model=PaymentResponse)
async def get_payment_status(
    ref: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get payment status by reference"""
    payment = db.query(Payment).filter(Payment.payment_reference == ref).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Users can only view their own payments
    if payment.booking.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this payment"
        )
    
    return payment


@router.post("/webhooks/mpesa")
async def mpesa_webhook(
    payload: dict,
    db: Session = Depends(get_db)
):
    """Handle M-Pesa webhook"""
    # TODO: Implement webhook signature verification
    # TODO: Process webhook payload and update payment status
    # TODO: Update booking payment_status when payment is completed
    
    # Placeholder implementation
    return {"message": "Webhook received"}


@router.post("/webhooks/flutterwave")
async def flutterwave_webhook(
    payload: dict,
    db: Session = Depends(get_db)
):
    """Handle Flutterwave webhook"""
    # TODO: Implement webhook signature verification
    # TODO: Process webhook payload and update payment status
    # TODO: Update booking payment_status when payment is completed
    
    # Placeholder implementation
    return {"message": "Webhook received"}

