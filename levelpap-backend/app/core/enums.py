from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    TRAINER = "trainer"


class CourseCategory(str, Enum):
    AI = "AI"
    ROBOTICS = "Robotics"
    DATA = "Data"
    IOT = "IoT"
    CYBERSECURITY = "Cybersecurity"
    BLOCKCHAIN = "Blockchain"
    DEVELOPMENT = "Development"


class Audience(str, Enum):
    KIDS = "Kids"
    ADULTS = "Adults"
    CORPORATE = "Corporate"


class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(str, Enum):
    MPESA = "mpesa"
    FLUTTERWAVE = "flutterwave"
    OTHER = "other"


class PaymentTransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CorporateRequestStatus(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    COMPLETED = "completed"

