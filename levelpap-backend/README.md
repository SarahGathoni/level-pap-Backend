# Tech Training Platform Backend

FastAPI backend for the Tech Training Platform, built according to the architecture specification.

## Features

- User authentication and authorization (JWT)
- Course and session management
- Booking system
- Payment integration (M-Pesa, Flutterwave)
- Corporate training requests
- Trainer management
- Role-based access control (Student, Trainer, Admin)

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Bcrypt** - Password hashing

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd levelpap-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
   - Database URL
   - Secret key (generate a secure random string)
   - Payment provider credentials (if using)

6. Initialize the database:
```bash
# Create database migrations
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

7. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
levelpap-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API route handlers
│   │       └── api.py         # Router aggregation
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   ├── enums.py           # Enum definitions
│   │   └── security.py        # Security utilities
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── main.py                # FastAPI application
├── alembic/                   # Database migrations
├── requirements.txt           # Python dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password
- `POST /api/auth/verify-email` - Verify email

### Courses
- `GET /api/courses` - List courses
- `GET /api/courses/{id}` - Get course details
- `POST /api/courses` - Create course (admin)
- `PUT /api/courses/{id}` - Update course (admin)
- `DELETE /api/courses/{id}` - Delete course (admin)

### Sessions
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{id}` - Get session details
- `GET /api/sessions/courses/{course_id}/sessions` - Get course sessions
- `POST /api/sessions` - Create session (admin)
- `PUT /api/sessions/{id}` - Update session (admin)
- `DELETE /api/sessions/{id}` - Cancel session (admin)

### Bookings
- `GET /api/bookings/users/{user_id}/bookings` - Get user bookings
- `GET /api/bookings/{id}` - Get booking details
- `POST /api/bookings` - Create booking
- `PUT /api/bookings/{id}/cancel` - Cancel booking
- `GET /api/bookings/sessions/{session_id}/bookings` - Get session bookings (admin)

### Payments
- `POST /api/payments/mpesa/initiate` - Initiate M-Pesa payment
- `POST /api/payments/flutterwave/initiate` - Initiate Flutterwave payment
- `GET /api/payments/status?ref={reference}` - Check payment status
- `POST /api/payments/webhooks/mpesa` - M-Pesa webhook
- `POST /api/payments/webhooks/flutterwave` - Flutterwave webhook

### Trainers
- `GET /api/trainers` - List trainers
- `GET /api/trainers/{id}` - Get trainer details
- `POST /api/trainers` - Create trainer (admin)
- `PUT /api/trainers/{id}` - Update trainer (admin)

### Users
- `GET /api/users` - List users (admin)
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Deactivate user (admin)

### Corporate Requests
- `POST /api/corporate/requests` - Submit request (public)
- `GET /api/corporate/requests` - List requests (admin)
- `GET /api/corporate/requests/{id}` - Get request details (admin)
- `PUT /api/corporate/requests/{id}` - Update request (admin)
- `DELETE /api/corporate/requests/{id}` - Delete request (admin)

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Development

### Running Tests
```bash
# Add pytest to requirements.txt and run:
pytest
```

### Code Formatting
```bash
# Install black and run:
black app/
```

## Environment Variables

See `.env.example` for all required environment variables.

## Security Notes

- Always use HTTPS in production
- Keep `SECRET_KEY` secure and never commit it
- Use strong passwords for database
- Regularly update dependencies
- Implement rate limiting for production
- Set up proper CORS origins

## TODO

- [ ] Implement actual M-Pesa integration
- [ ] Implement actual Flutterwave integration
- [ ] Add email service for notifications
- [ ] Add background job processing
- [ ] Add caching layer
- [ ] Add comprehensive tests
- [ ] Add logging and monitoring
- [ ] Add API rate limiting

## License

[Your License Here]

