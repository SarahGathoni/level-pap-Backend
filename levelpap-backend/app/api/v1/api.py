from fastapi import APIRouter
from app.api.v1.endpoints import auth, courses, sessions, bookings, payments, trainers, users, corporate

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(trainers.router, prefix="/trainers", tags=["Trainers"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(corporate.router, prefix="/corporate", tags=["Corporate Requests"])

