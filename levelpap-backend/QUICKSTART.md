# Quick Start Guide

## Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/levelpap_db
SECRET_KEY=your-secret-key-here-generate-a-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Create Database
```bash
# Connect to PostgreSQL and create database
createdb levelpap_db
```

### 4. Run Migrations
```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Start Server
```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload
```

### 6. Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing the API

### Register a User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "Test User",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

### Get Current User (with token)
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env` file
- Verify database exists

### Migration Errors
- Make sure all models are imported in `alembic/env.py`
- Check that database URL is correct

### Import Errors
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check that all dependencies are installed

