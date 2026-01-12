# Backend Setup & Architecture Explanation

This document explains the complete backend setup process, file organization, and architectural decisions for the Tech Training Platform backend.

---

## Table of Contents
1. [Initial Setup Order](#initial-setup-order)
2. [Project Structure Overview](#project-structure-overview)
3. [Core Foundation Layer](#core-foundation-layer)
4. [Data Layer (Models)](#data-layer-models)
5. [Schema Layer](#schema-layer)
6. [API Layer](#api-layer)
7. [Data Flow: Models → Schemas → API](#data-flow-models--schemas--api)
8. [Why This Architecture?](#why-this-architecture)

---

## Initial Setup Order

### Phase 1: Project Foundation (Setup First)

#### 1. **`requirements.txt`** ⭐ FIRST FILE
**Why first?** Defines all dependencies needed for the project.

**What it does:**
- Lists all Python packages (FastAPI, SQLAlchemy, Alembic, etc.)
- Ensures consistent environment across developers
- Used by `pip install -r requirements.txt`

**Key dependencies:**
- `fastapi` - Web framework
- `sqlalchemy` - ORM for database
- `alembic` - Database migrations
- `psycopg[binary]` - PostgreSQL driver
- `pydantic` - Data validation
- `python-jose` - JWT tokens
- `passlib[bcrypt]` - Password hashing

---

#### 2. **`.env` file** (Create manually)
**Why second?** Contains environment-specific configuration.

**What it does:**
- Stores sensitive data (database URL, secret keys)
- Keeps configuration out of code
- Different values for dev/staging/production

**Required variables:**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/levelpap_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

#### 3. **`app/core/config.py`** ⭐ FOUNDATION FILE
**Why third?** Central configuration that everything else depends on.

**What it does:**
- Loads environment variables from `.env`
- Provides `settings` object used throughout the app
- Validates configuration values
- Parses CORS origins, payment provider keys, etc.

**Key features:**
- Uses `pydantic-settings` for validation
- Single source of truth for all settings
- Type-safe configuration

---

#### 4. **`app/core/database.py`** ⭐ FOUNDATION FILE
**Why fourth?** Database connection setup required before models.

**What it does:**
- Creates SQLAlchemy engine (connection pool)
- Defines `SessionLocal` for database sessions
- Provides `Base` class for all models
- Exports `get_db()` dependency for FastAPI

**Key components:**
```python
engine = create_engine(...)  # Connection pool
SessionLocal = sessionmaker(...)  # Session factory
Base = declarative_base()  # Base for all models
get_db()  # Dependency injection function
```

---

#### 5. **`app/core/enums.py`** ⭐ FOUNDATION FILE
**Why fifth?** Defines constants used by models and schemas.

**What it does:**
- Defines all enum types (UserRole, CourseCategory, etc.)
- Ensures type safety and consistency
- Used by both SQLAlchemy models and Pydantic schemas

**Enums defined:**
- `UserRole`: student, admin, trainer
- `CourseCategory`: AI, Robotics, Data, etc.
- `Audience`: Kids, Adults, Corporate
- `SessionStatus`, `PaymentStatus`, etc.

---

#### 6. **`app/core/security.py`** ⭐ FOUNDATION FILE
**Why sixth?** Authentication utilities needed by auth endpoints.

**What it does:**
- Password hashing/verification (bcrypt)
- JWT token creation/decoding
- Cryptographic operations

**Functions:**
- `get_password_hash()` - Hash passwords
- `verify_password()` - Verify passwords
- `create_access_token()` - Generate JWT
- `decode_access_token()` - Validate JWT

---

#### 7. **`app/core/dependencies.py`** ⭐ FOUNDATION FILE
**Why seventh?** Authentication dependencies used by API endpoints.

**What it does:**
- Provides `get_current_user()` - Extract user from JWT
- Provides `get_current_active_user()` - Ensure user is active
- Provides `require_role()` - Role-based access control
- Pre-built dependencies: `require_admin`, `require_trainer`

**How it works:**
- Uses FastAPI's `Depends()` for dependency injection
- Validates JWT tokens
- Checks user permissions
- Used as dependencies in route handlers

---

### Phase 2: Application Structure

#### 8. **`app/__init__.py`** (Empty file)
**Why?** Makes `app` a Python package.

**What it does:**
- Allows imports like `from app.models import User`
- Marks directory as a package

---

#### 9. **`app/main.py`** ⭐ APPLICATION ENTRY POINT
**Why ninth?** FastAPI application instance.

**What it does:**
- Creates FastAPI app instance
- Configures CORS middleware
- Includes API router
- Defines root and health endpoints

**Key features:**
- App metadata (title, version, docs)
- CORS configuration
- Router mounting at `/api`

---

### Phase 3: Database Layer

#### 10. **`app/models/`** folder ⭐ DATA LAYER
**Why tenth?** Database models define the schema.

**Setup order within models:**
1. `app/models/user.py` - Base user model (referenced by others)
2. `app/models/trainer.py` - Trainer model (references User)
3. `app/models/course.py` - Course model (references Trainer)
4. `app/models/session.py` - Session model (references Course)
5. `app/models/booking.py` - Booking model (references User, Session)
6. `app/models/payment.py` - Payment model (references Booking)
7. `app/models/corporate_request.py` - Corporate requests

**What models do:**
- Define database tables using SQLAlchemy
- Define relationships between entities
- Define constraints and indexes
- Map Python classes to database tables

**Example structure:**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True)
    # ... more fields
```

---

#### 11. **`app/models/__init__.py`**
**Why?** Imports all models for Alembic migrations.

**What it does:**
- Imports all model classes
- Makes models discoverable by Alembic
- Required for `alembic revision --autogenerate`

---

### Phase 4: Schema Layer

#### 12. **`app/schemas/`** folder ⭐ VALIDATION LAYER
**Why twelfth?** Pydantic schemas for request/response validation.

**Setup order:**
- Create schemas matching models (one schema file per model)
- `auth.py` - Authentication schemas
- `user.py` - User schemas
- `course.py` - Course schemas
- etc.

**What schemas do:**
- Validate incoming request data
- Serialize response data
- Define API contracts
- Type safety for API endpoints

**Common schema patterns:**
- `XxxBase` - Common fields
- `XxxCreate` - Fields for creation
- `XxxUpdate` - Fields for updates (all optional)
- `XxxResponse` - Fields returned to client

---

### Phase 5: API Layer

#### 13. **`app/api/v1/api.py`** ⭐ API ROUTER
**Why thirteenth?** Aggregates all endpoint routers.

**What it does:**
- Creates main API router
- Includes all endpoint routers
- Defines API versioning (`/api/v1/`)

**Structure:**
```python
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(courses.router, prefix="/courses")
# ... etc
```

---

#### 14. **`app/api/v1/endpoints/`** folder ⭐ ENDPOINT LAYER
**Why fourteenth?** Individual endpoint files.

**What endpoints do:**
- Define HTTP routes (GET, POST, PUT, DELETE)
- Handle request/response logic
- Use dependencies for auth/permissions
- Call database operations
- Return validated responses

**File structure:**
- `auth.py` - Authentication endpoints
- `courses.py` - Course CRUD operations
- `sessions.py` - Session management
- `bookings.py` - Booking operations
- `payments.py` - Payment processing
- `trainers.py` - Trainer management
- `users.py` - User management
- `corporate.py` - Corporate requests

---

### Phase 6: Database Migrations

#### 15. **`alembic.ini`** ⭐ MIGRATION CONFIG
**Why fifteenth?** Alembic configuration for migrations.

**What it does:**
- Configures Alembic migration tool
- Sets migration script location
- Configures logging

---

#### 16. **`alembic/env.py`** ⭐ MIGRATION SETUP
**Why sixteenth?** Migration environment setup.

**What it does:**
- Imports all models (required!)
- Sets database URL from settings
- Configures migration metadata
- Handles online/offline migrations

**Critical:** Must import all models here:
```python
from app.models import *  # This is why models/__init__.py exists!
```

---

### Phase 7: Execution

#### 17. **`run.py`** ⭐ SERVER RUNNER
**Why last?** Entry point to run the server.

**What it does:**
- Starts Uvicorn server
- Points to `app.main:app`
- Configures reload for development
- Sets host/port

---

## Project Structure Overview

```
levelpap-backend/
├── app/                          # Main application package
│   ├── __init__.py              # Package marker
│   ├── main.py                  # FastAPI app instance
│   │
│   ├── core/                    # Core/foundation layer
│   │   ├── __init__.py
│   │   ├── config.py           # Settings & configuration
│   │   ├── database.py         # Database connection & session
│   │   ├── dependencies.py     # Auth dependencies
│   │   ├── enums.py            # Enum definitions
│   │   └── security.py         # Password & JWT utilities
│   │
│   ├── models/                  # Database models (SQLAlchemy)
│   │   ├── __init__.py         # Model exports
│   │   ├── user.py             # User model
│   │   ├── trainer.py          # Trainer model
│   │   ├── course.py           # Course model
│   │   ├── session.py          # Session model
│   │   ├── booking.py          # Booking model
│   │   ├── payment.py          # Payment model
│   │   └── corporate_request.py # Corporate request model
│   │
│   ├── schemas/                 # Pydantic schemas (validation)
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth schemas
│   │   ├── user.py             # User schemas
│   │   ├── course.py           # Course schemas
│   │   ├── session.py          # Session schemas
│   │   ├── booking.py          # Booking schemas
│   │   ├── payment.py          # Payment schemas
│   │   ├── trainer.py          # Trainer schemas
│   │   └── corporate_request.py # Corporate request schemas
│   │
│   └── api/                     # API endpoints
│       ├── __init__.py
│       └── v1/                  # API version 1
│           ├── __init__.py
│           ├── api.py          # Main API router
│           └── endpoints/      # Individual endpoint files
│               ├── __init__.py
│               ├── auth.py      # Auth endpoints
│               ├── courses.py  # Course endpoints
│               ├── sessions.py # Session endpoints
│               ├── bookings.py # Booking endpoints
│               ├── payments.py # Payment endpoints
│               ├── trainers.py # Trainer endpoints
│               ├── users.py    # User endpoints
│               └── corporate.py # Corporate endpoints
│
├── alembic/                     # Database migrations
│   ├── env.py                  # Migration environment
│   ├── versions/               # Migration files
│   └── script.py.mako          # Migration template
│
├── scripts/                     # Utility scripts
│   └── init_db.py              # Database initialization
│
├── requirements.txt             # Python dependencies
├── alembic.ini                 # Alembic configuration
├── run.py                      # Server runner
├── .env                        # Environment variables (not in git)
└── .gitignore                  # Git ignore rules
```

---

## Core Foundation Layer

### Purpose
The `app/core/` folder contains foundational code that everything else depends on. These files are set up FIRST because they provide infrastructure.

### Files Explained

#### `config.py` - Configuration Management
**Purpose:** Centralized configuration loading and validation.

**Key features:**
- Loads from `.env` file
- Validates all settings
- Provides `settings` singleton object
- Type-safe configuration

**Usage:**
```python
from app.core.config import settings
database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
```

---

#### `database.py` - Database Connection
**Purpose:** SQLAlchemy engine and session management.

**Key components:**
- `engine` - Database connection pool
- `SessionLocal` - Session factory
- `Base` - Base class for all models
- `get_db()` - FastAPI dependency for database sessions

**Usage:**
```python
from app.core.database import Base, get_db
from sqlalchemy.orm import Session

def my_endpoint(db: Session = Depends(get_db)):
    # Use db session
    pass
```

---

#### `security.py` - Authentication Utilities
**Purpose:** Password hashing and JWT token management.

**Functions:**
- `get_password_hash()` - Hash passwords with bcrypt
- `verify_password()` - Verify password against hash
- `create_access_token()` - Generate JWT tokens
- `decode_access_token()` - Validate and decode JWT

**Usage:**
```python
from app.core.security import get_password_hash, create_access_token
hashed = get_password_hash("password123")
token = create_access_token({"sub": user_id})
```

---

#### `dependencies.py` - FastAPI Dependencies
**Purpose:** Reusable dependencies for authentication and authorization.

**Key dependencies:**
- `get_current_user()` - Extract user from JWT token
- `get_current_active_user()` - Ensure user is active
- `require_role()` - Role-based access control factory
- `require_admin` - Pre-built admin-only dependency
- `require_trainer` - Pre-built trainer/admin dependency

**Usage:**
```python
from app.core.dependencies import get_current_active_user, require_admin

@router.get("/admin-only")
async def admin_endpoint(user: User = Depends(require_admin)):
    # Only admins can access
    pass
```

---

#### `enums.py` - Enum Definitions
**Purpose:** Centralized enum definitions for type safety.

**Enums:**
- `UserRole` - User roles (student, admin, trainer)
- `CourseCategory` - Course categories
- `Audience` - Target audience types
- `SessionStatus` - Session statuses
- `PaymentStatus` - Payment statuses
- etc.

**Usage:**
```python
from app.core.enums import UserRole
user.role = UserRole.ADMIN
```

---

## Data Layer (Models)

### Purpose
The `app/models/` folder contains SQLAlchemy models that define database tables and relationships.

### Architecture Pattern: Database-First Design

**Models define:**
1. **Table structure** - Columns, types, constraints
2. **Relationships** - Foreign keys, one-to-many, many-to-one
3. **Indexes** - For query performance
4. **Business rules** - Constraints at database level

### Model Files Explained

#### `user.py` - User Model
**Purpose:** User accounts and authentication.

**Key fields:**
- `id` - UUID primary key
- `email` - Unique, indexed
- `password_hash` - Hashed password
- `role` - UserRole enum
- `is_active` - Soft delete flag
- `email_verified` - Email verification status

**Relationships:**
- One-to-many with Bookings
- Optional one-to-one with Trainer

---

#### `trainer.py` - Trainer Model
**Purpose:** Trainer profiles.

**Key fields:**
- `id` - UUID primary key
- `user_id` - Optional foreign key to User
- `name`, `bio`, `photo`
- `specializations` - Array of strings
- `rating` - Average rating

**Relationships:**
- Optional one-to-one with User
- One-to-many with Courses
- One-to-many with Sessions

---

#### `course.py` - Course Model
**Purpose:** Course catalog.

**Key fields:**
- `id` - UUID primary key
- `title`, `description`
- `category` - CourseCategory enum
- `audience` - Audience enum
- `price` - Decimal
- `syllabus` - Array of strings
- `is_published` - Visibility flag
- `trainer_id` - Foreign key to Trainer

**Relationships:**
- Many-to-one with Trainer
- One-to-many with Sessions

---

#### `session.py` - Session Model
**Purpose:** Individual training sessions.

**Key fields:**
- `id` - UUID primary key
- `course_id` - Foreign key to Course
- `date`, `start_time`, `end_time`
- `location`
- `capacity`, `seats_booked`
- `status` - SessionStatus enum

**Relationships:**
- Many-to-one with Course
- Many-to-one with Trainer (optional override)
- One-to-many with Bookings

---

#### `booking.py` - Booking Model
**Purpose:** User session bookings.

**Key fields:**
- `id` - UUID primary key
- `user_id` - Foreign key to User
- `session_id` - Foreign key to Session
- `seats` - Number of seats
- `payment_status` - PaymentStatus enum
- `total_amount` - Calculated price

**Relationships:**
- Many-to-one with User
- Many-to-one with Session
- One-to-one with Payment

---

#### `payment.py` - Payment Model
**Purpose:** Payment transactions.

**Key fields:**
- `id` - UUID primary key
- `booking_id` - Foreign key to Booking (unique)
- `provider` - PaymentProvider enum
- `payment_reference` - Unique reference
- `amount`, `currency`
- `status` - PaymentTransactionStatus enum
- `provider_transaction_id` - External transaction ID

**Relationships:**
- One-to-one with Booking

---

#### `corporate_request.py` - Corporate Request Model
**Purpose:** Corporate training requests.

**Key fields:**
- `id` - UUID primary key
- `company_name`, `contact_person`
- `email`, `phone`
- `topic`, `preferred_dates`
- `status` - CorporateRequestStatus enum
- `assigned_to_trainer_id` - Foreign key to Trainer

**Relationships:**
- Many-to-one with Trainer (optional)
- Many-to-one with User (admin responder)

---

### Model Relationships Summary

```
User (1) ────────< (0..1) Trainer
  │                      │
  │                      │ (1)
  │                      │
  │                      ▼
  │                  Course (1)
  │                      │
  │                      │ (1)
  │                      │
  │                      ▼
  │                  Session (1)
  │                      │
  │                      │ (1)
  │                      │
  │                      ▼
  │                  Booking (1) ────< (1) Payment
  │                      │
  │                      │ (N)
  │                      │
  │                      ▼
  │                  User
```

---

## Schema Layer

### Purpose
The `app/schemas/` folder contains Pydantic models for request/response validation and serialization.

### Architecture Pattern: Separation of Concerns

**Why separate schemas from models?**
1. **Models** = Database structure (SQLAlchemy)
2. **Schemas** = API contracts (Pydantic)
3. **Different purposes** - Models for DB, Schemas for API

### Schema Patterns

#### Base Schema
Common fields shared across operations.

```python
class CourseBase(BaseModel):
    title: str
    category: CourseCategory
    description: str
```

#### Create Schema
Fields required for creation (inherits from Base).

```python
class CourseCreate(CourseBase):
    trainer_id: Optional[UUID] = None
```

#### Update Schema
All fields optional (for partial updates).

```python
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[CourseCategory] = None
    # ... all optional
```

#### Response Schema
Fields returned to client (includes IDs, timestamps).

```python
class CourseResponse(CourseBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model
```

### Schema Files Explained

#### `auth.py` - Authentication Schemas
- `Token` - JWT token response
- `TokenData` - Token payload data
- `UserWithToken` - User + token response

#### `user.py` - User Schemas
- `UserBase` - Common user fields
- `UserCreate` - Registration data
- `UserUpdate` - Profile update data
- `UserResponse` - User data returned to client

#### `course.py` - Course Schemas
- `CourseBase` - Common course fields
- `CourseCreate` - Course creation data
- `CourseUpdate` - Course update data
- `CourseResponse` - Course data returned to client

**Similar patterns for:** `session.py`, `booking.py`, `payment.py`, etc.

---

## API Layer

### Purpose
The `app/api/` folder contains FastAPI route handlers that expose HTTP endpoints.

### Architecture Pattern: Layered API Design

**Structure:**
```
app/api/v1/
├── api.py              # Main router (aggregates all endpoints)
└── endpoints/          # Individual endpoint files
    ├── auth.py         # Authentication routes
    ├── courses.py      # Course CRUD routes
    └── ...
```

### API Router (`api.py`)

**Purpose:** Aggregates all endpoint routers into one main router.

**Structure:**
```python
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
# ... etc
```

**Benefits:**
- Centralized routing
- Version management (`/api/v1/`)
- Organized tags for documentation

---

### Endpoint Files (`endpoints/`)

**Purpose:** Individual route handlers for each resource.

#### Standard CRUD Pattern

**Example: `courses.py`**

```python
router = APIRouter()

# READ - List all
@router.get("", response_model=List[CourseResponse])
async def list_courses(...):
    # Query database
    # Return list

# READ - Get one
@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(...):
    # Query database
    # Return single item

# CREATE
@router.post("", response_model=CourseResponse, status_code=201)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(require_admin),  # Auth check
    db: Session = Depends(get_db)
):
    # Create model instance
    # Save to database
    # Return created item

# UPDATE
@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(...):
    # Find existing item
    # Update fields
    # Save changes
    # Return updated item

# DELETE
@router.delete("/{course_id}", status_code=204)
async def delete_course(...):
    # Find item
    # Soft delete (set is_active=False)
    # Return success
```

#### Endpoint Files Explained

**`auth.py`** - Authentication endpoints
- `POST /register` - User registration
- `POST /login` - User login (returns JWT)
- `GET /me` - Get current user
- `POST /logout` - Logout (client discards token)
- `POST /forgot-password` - Request password reset
- `POST /reset-password` - Reset password with token
- `POST /verify-email` - Verify email with token

**`courses.py`** - Course management
- `GET /courses` - List courses (with filters)
- `GET /courses/{id}` - Get course details
- `POST /courses` - Create course (admin only)
- `PUT /courses/{id}` - Update course (admin only)
- `DELETE /courses/{id}` - Delete course (admin only)

**`sessions.py`** - Session management
- `GET /sessions` - List sessions
- `GET /sessions/{id}` - Get session details
- `POST /sessions` - Create session (admin)
- `PUT /sessions/{id}` - Update session (admin)
- `DELETE /sessions/{id}` - Cancel session (admin)

**`bookings.py`** - Booking operations
- `GET /bookings` - List user's bookings
- `GET /bookings/{id}` - Get booking details
- `POST /bookings` - Create booking (authenticated)
- `PUT /bookings/{id}/cancel` - Cancel booking

**`payments.py`** - Payment processing
- `POST /payments/mpesa/initiate` - Initiate M-Pesa payment
- `POST /payments/flutterwave/initiate` - Initiate Flutterwave payment
- `GET /payments/status` - Check payment status
- `POST /payments/webhooks/mpesa` - M-Pesa webhook
- `POST /payments/webhooks/flutterwave` - Flutterwave webhook

**`trainers.py`** - Trainer management
- `GET /trainers` - List trainers
- `GET /trainers/{id}` - Get trainer details
- `POST /trainers` - Create trainer (admin)
- `PUT /trainers/{id}` - Update trainer (admin)

**`users.py`** - User management (admin)
- `GET /users` - List users (admin)
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Deactivate user (admin)

**`corporate.py`** - Corporate requests
- `POST /corporate/requests` - Submit request (public)
- `GET /corporate/requests` - List requests (admin)
- `GET /corporate/requests/{id}` - Get request details
- `PUT /corporate/requests/{id}` - Update status (admin)

---

## Data Flow: Models → Schemas → API

### Complete Request Flow

#### Example: Creating a Course

**1. Client sends HTTP request:**
```http
POST /api/courses
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Python Basics",
  "category": "Development",
  "audience": "Adults",
  "description": "Learn Python...",
  "price": 5000.00,
  "syllabus": ["Intro", "Variables", "Functions"]
}
```

**2. FastAPI receives request:**
- `main.py` → routes to `/api/courses`
- `api.py` → routes to `courses.router`
- `endpoints/courses.py` → `create_course()` handler

**3. Authentication check:**
```python
current_user: User = Depends(require_admin)
```
- `dependencies.py` → `require_admin()` checks JWT
- `security.py` → `decode_access_token()` validates token
- Returns `User` object if valid

**4. Request validation:**
```python
course_data: CourseCreate
```
- Pydantic validates JSON against `CourseCreate` schema
- Type checking, field validation
- Converts to `CourseCreate` object

**5. Database operation:**
```python
course = Course(**course_data.dict())
db.add(course)
db.commit()
```
- Creates SQLAlchemy `Course` model instance
- Adds to database session
- Commits transaction

**6. Response serialization:**
```python
response_model=CourseResponse
```
- Converts SQLAlchemy model → Pydantic schema
- Serializes to JSON
- Returns to client

**7. Client receives response:**
```json
{
  "id": "uuid-here",
  "title": "Python Basics",
  "category": "Development",
  "created_at": "2024-01-01T00:00:00Z",
  ...
}
```

---

### Data Transformation Layers

```
HTTP Request (JSON)
    ↓
Pydantic Schema (CourseCreate)  ← Validation
    ↓
SQLAlchemy Model (Course)        ← Database
    ↓
Pydantic Schema (CourseResponse) ← Serialization
    ↓
HTTP Response (JSON)
```

**Why this separation?**
1. **Schemas** validate API contracts
2. **Models** handle database operations
3. **Endpoints** orchestrate the flow
4. **Clear separation** of concerns

---

## Why This Architecture?

### 1. **Separation of Concerns**
- **Models** = Database layer
- **Schemas** = API layer
- **Endpoints** = Business logic layer
- **Core** = Infrastructure layer

### 2. **Scalability**
- Easy to add new endpoints
- Easy to version APIs (`/api/v1/`, `/api/v2/`)
- Modular structure

### 3. **Type Safety**
- Pydantic validates requests
- SQLAlchemy ensures database integrity
- Type hints throughout

### 4. **Testability**
- Each layer can be tested independently
- Dependencies can be mocked
- Clear interfaces between layers

### 5. **Maintainability**
- Clear file organization
- Consistent patterns
- Easy to find code

### 6. **Security**
- Authentication at dependency level
- Role-based access control
- Input validation via schemas

### 7. **Database Migrations**
- Alembic tracks schema changes
- Version-controlled migrations
- Easy rollback

---

## Key Architectural Decisions

### 1. **Why Models Separate from Schemas?**
- **Models** define database structure (SQLAlchemy)
- **Schemas** define API contracts (Pydantic)
- Different purposes, different libraries
- Allows API to evolve independently from database

### 2. **Why Core Folder?**
- Centralizes infrastructure code
- Single source of truth for config
- Reusable across the application
- Foundation that everything builds on

### 3. **Why API Versioning (`/api/v1/`)?**
- Allows breaking changes in future
- Multiple API versions can coexist
- Gradual migration path
- Industry best practice

### 4. **Why Dependency Injection?**
- `get_db()` - Database session management
- `get_current_user()` - Authentication
- `require_admin` - Authorization
- Testable, reusable, clean code

### 5. **Why Soft Deletes?**
- `is_active` flag instead of hard delete
- Preserves data integrity
- Audit trail
- Can restore if needed

### 6. **Why UUID Primary Keys?**
- Globally unique identifiers
- Better for distributed systems
- Don't reveal information (sequential IDs do)
- Industry standard

---

## Summary: Setup Checklist

### ✅ Phase 1: Foundation (Do First)
1. Create `requirements.txt`
2. Create `.env` file
3. Create `app/core/config.py`
4. Create `app/core/database.py`
5. Create `app/core/enums.py`
6. Create `app/core/security.py`
7. Create `app/core/dependencies.py`

### ✅ Phase 2: Application Structure
8. Create `app/__init__.py`
9. Create `app/main.py`

### ✅ Phase 3: Database Layer
10. Create `app/models/` folder
11. Create models (user → trainer → course → session → booking → payment)
12. Create `app/models/__init__.py` (import all models)

### ✅ Phase 4: Schema Layer
13. Create `app/schemas/` folder
14. Create schemas matching models

### ✅ Phase 5: API Layer
15. Create `app/api/v1/api.py`
16. Create `app/api/v1/endpoints/` folder
17. Create endpoint files

### ✅ Phase 6: Migrations
18. Create `alembic.ini`
19. Configure `alembic/env.py`
20. Run initial migration

### ✅ Phase 7: Execution
21. Create `run.py`
22. Test the server

---

## Next Steps After Setup

1. **Run migrations:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

2. **Start server:**
   ```bash
   python run.py
   ```

3. **Test API:**
   - Visit `http://localhost:8000/docs`
   - Test endpoints via Swagger UI

4. **Add features:**
   - Follow the same patterns
   - Model → Schema → Endpoint
   - Use dependencies for auth

---

This architecture provides a solid foundation for a scalable, maintainable backend API! 🚀

