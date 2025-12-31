# Backend Architecture Documentation

## Overview
This document outlines the backend architecture for the Tech Training Platform, including database design, models, relationships, and core business logic. The architecture is language-agnostic and can be implemented using any backend framework.

---

## Database Schema

### Core Entities

#### 1. **Users Table**
Stores user account information and authentication data.

**Fields:**
- `id` (Primary Key, UUID/String)
- `email` (String, Unique, Indexed)
- `password_hash` (String, Encrypted)
- `name` (String)
- `phone` (String, Optional)
- `role` (Enum: 'student', 'admin', 'trainer', Default: 'student')
- `email_verified` (Boolean, Default: false)
- `email_verification_token` (String, Optional, Indexed)
- `password_reset_token` (String, Optional, Indexed)
- `password_reset_expires` (DateTime, Optional)
- `created_at` (DateTime, Indexed)
- `updated_at` (DateTime)
- `last_login` (DateTime, Optional)
- `is_active` (Boolean, Default: true)

**Indexes:**
- Primary: `id`
- Unique: `email`
- Index: `email_verification_token`
- Index: `password_reset_token`
- Index: `created_at`

---

#### 2. **Trainers Table**
Stores trainer profile information.

**Fields:**
- `id` (Primary Key, UUID/String)
- `user_id` (Foreign Key → Users.id, Unique, Nullable)
- `name` (String)
- `bio` (Text, Optional)
- `photo` (String/URL, Optional)
- `specializations` (Array/JSON, Optional) - e.g., ["AI", "Robotics"]
- `years_of_experience` (Integer, Optional)
- `certifications` (Array/JSON, Optional)
- `rating` (Decimal, Optional) - Average rating from course reviews
- `total_courses_taught` (Integer, Default: 0)
- `is_active` (Boolean, Default: true)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Unique: `user_id`
- Index: `is_active`

**Relationships:**
- One-to-One with Users (optional - trainers can have user accounts)
- One-to-Many with Courses

---

#### 3. **Courses Table**
Stores course catalog information.

**Fields:**
- `id` (Primary Key, UUID/String)
- `title` (String, Indexed)
- `category` (Enum: 'AI', 'Robotics', 'Data', 'IoT', 'Cybersecurity', 'Blockchain', 'Development')
- `audience` (Enum: 'Kids', 'Adults', 'Corporate')
- `description` (Text)
- `duration_weeks` (Integer, Optional)
- `price` (Decimal, Optional) - Base price per seat
- `syllabus` (Array/JSON) - List of topics/modules
- `image` (String/URL, Optional)
- `trainer_id` (Foreign Key → Trainers.id, Optional)
- `is_published` (Boolean, Default: false)
- `is_active` (Boolean, Default: true)
- `created_at` (DateTime, Indexed)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Index: `category`
- Index: `audience`
- Index: `trainer_id`
- Index: `is_published`
- Index: `is_active`
- Full-text: `title`, `description` (for search)

**Relationships:**
- Many-to-One with Trainers
- One-to-Many with Sessions

---

#### 4. **Sessions Table**
Stores individual training session instances.

**Fields:**
- `id` (Primary Key, UUID/String)
- `course_id` (Foreign Key → Courses.id, Indexed)
- `date` (Date, Indexed)
- `start_time` (Time)
- `end_time` (Time, Optional)
- `location` (String)
- `trainer_id` (Foreign Key → Trainers.id, Optional) - Can override course trainer
- `capacity` (Integer, Default: 1)
- `seats_booked` (Integer, Default: 0) - Calculated from bookings
- `status` (Enum: 'scheduled', 'ongoing', 'completed', 'cancelled', Default: 'scheduled')
- `notes` (Text, Optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Index: `course_id`
- Index: `date`
- Index: `trainer_id`
- Index: `status`
- Composite: `(course_id, date)` - For finding sessions by course and date

**Relationships:**
- Many-to-One with Courses
- Many-to-One with Trainers (optional override)
- One-to-Many with Bookings

**Computed Fields:**
- `seats_left` = `capacity - seats_booked` (calculated, not stored)

---

#### 5. **Bookings Table**
Stores user session bookings.

**Fields:**
- `id` (Primary Key, UUID/String)
- `user_id` (Foreign Key → Users.id, Indexed)
- `session_id` (Foreign Key → Sessions.id, Indexed)
- `seats` (Integer, Default: 1, Min: 1)
- `payment_status` (Enum: 'pending', 'paid', 'failed', 'refunded', Default: 'pending')
- `total_amount` (Decimal) - Calculated: seats × session.course.price
- `contact_phone` (String, Optional) - For booking confirmation
- `special_requirements` (Text, Optional)
- `cancelled_at` (DateTime, Optional)
- `cancellation_reason` (Text, Optional)
- `created_at` (DateTime, Indexed)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Index: `user_id`
- Index: `session_id`
- Index: `payment_status`
- Index: `created_at`
- Composite: `(user_id, session_id)` - Prevent duplicate bookings

**Relationships:**
- Many-to-One with Users
- Many-to-One with Sessions
- One-to-One with Payments

**Business Rules:**
- Cannot book more seats than available (`seats <= session.seats_left`)
- Cannot create duplicate booking for same user and session
- `total_amount` = `seats × course.price` (calculated on creation)

---

#### 6. **Payments Table**
Stores payment transaction records.

**Fields:**
- `id` (Primary Key, UUID/String)
- `booking_id` (Foreign Key → Bookings.id, Unique, Indexed)
- `provider` (Enum: 'mpesa', 'flutterwave', 'other')
- `payment_reference` (String, Unique, Indexed) - External payment reference
- `amount` (Decimal)
- `currency` (String, Default: 'KES')
- `status` (Enum: 'pending', 'processing', 'completed', 'failed', 'cancelled', Default: 'pending')
- `provider_response` (JSON, Optional) - Store full provider response
- `provider_transaction_id` (String, Optional, Indexed)
- `initiated_at` (DateTime)
- `completed_at` (DateTime, Optional)
- `failure_reason` (Text, Optional)
- `metadata` (JSON, Optional) - Additional payment data
- `created_at` (DateTime, Indexed)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Unique: `booking_id`
- Unique: `payment_reference`
- Index: `provider_transaction_id`
- Index: `status`
- Index: `created_at`

**Relationships:**
- One-to-One with Bookings

**Business Rules:**
- One payment per booking
- Payment amount must match booking total_amount
- Status transitions: pending → processing → completed/failed

---

#### 7. **Corporate Requests Table**
Stores corporate training requests.

**Fields:**
- `id` (Primary Key, UUID/String)
- `company_name` (String, Indexed)
- `contact_person` (String)
- `email` (String, Indexed)
- `phone` (String)
- `topic` (String)
- `preferred_dates` (Array/JSON) - List of date strings
- `preferred_time` (String, Optional) - e.g., "09:00-17:00"
- `location` (String, Optional)
- `headcount` (Integer, Optional)
- `notes` (Text, Optional)
- `status` (Enum: 'pending', 'reviewing', 'confirmed', 'rejected', 'completed', Default: 'pending')
- `assigned_to_trainer_id` (Foreign Key → Trainers.id, Optional)
- `quoted_price` (Decimal, Optional)
- `admin_notes` (Text, Optional) - Internal notes
- `responded_at` (DateTime, Optional)
- `responded_by` (Foreign Key → Users.id, Optional) - Admin user
- `created_at` (DateTime, Indexed)
- `updated_at` (DateTime)

**Indexes:**
- Primary: `id`
- Index: `email`
- Index: `status`
- Index: `assigned_to_trainer_id`
- Index: `created_at`

**Relationships:**
- Many-to-One with Trainers (optional assignment)
- Many-to-One with Users (admin responder)

---

#### 8. **Payment Webhooks Table** (Optional but Recommended)
Stores payment provider webhook events for audit and reconciliation.

**Fields:**
- `id` (Primary Key, UUID/String)
- `payment_id` (Foreign Key → Payments.id, Optional)
- `provider` (Enum: 'mpesa', 'flutterwave')
- `event_type` (String) - e.g., 'payment.success', 'payment.failed'
- `payload` (JSON) - Full webhook payload
- `processed` (Boolean, Default: false)
- `processing_error` (Text, Optional)
- `created_at` (DateTime, Indexed)

**Indexes:**
- Primary: `id`
- Index: `payment_id`
- Index: `processed`
- Index: `created_at`

**Relationships:**
- Many-to-One with Payments (optional)

---

## Entity Relationship Diagram (ERD)

```
Users (1) ────────< (0..1) Trainers
  │                      │
  │                      │
  │ (1)                  │ (1)
  │                      │
  │                      │
  │                      ▼
  │                  Courses (1)
  │                      │
  │                      │ (1)
  │                      │
  │                      ▼
  │                  Sessions (1)
  │                      │
  │                      │ (1)
  │                      │
  │                      ▼
  │                  Bookings (1) ────< (1) Payments
  │                      │
  │                      │ (N)
  │                      │
  │                      ▼
  │                  Users
  │
  │ (1)
  │
  ▼
Corporate Requests (N) ────< (0..1) Trainers
  │
  │ (1)
  │
  ▼
Users (admin responder)
```

---

## Relationships Summary

### One-to-Many Relationships:
1. **Users → Bookings**: One user can have many bookings
2. **Users → Corporate Requests**: One admin can respond to many requests
3. **Trainers → Courses**: One trainer can teach many courses
4. **Trainers → Sessions**: One trainer can conduct many sessions
5. **Courses → Sessions**: One course can have many sessions
6. **Sessions → Bookings**: One session can have many bookings

### One-to-One Relationships:
1. **Users ↔ Trainers**: Optional - A trainer can have a user account
2. **Bookings ↔ Payments**: One booking has one payment

### Many-to-Many (Implicit):
- **Users ↔ Courses** (through Bookings and Sessions)
- **Trainers ↔ Users** (through Courses and Bookings)

---

## Business Rules & Constraints

### Booking Rules:
1. **Seat Availability**: Cannot book more seats than `session.seats_left`
2. **Duplicate Prevention**: Same user cannot book the same session twice
3. **Payment Requirement**: Booking must have payment before session starts
4. **Cancellation**: Cancelled bookings free up seats immediately

### Session Rules:
1. **Capacity Management**: `seats_booked` is calculated from confirmed bookings (payment_status = 'paid')
2. **Date Validation**: Session date must be in the future (for new sessions)
3. **Trainer Assignment**: If session has no trainer_id, use course.trainer_id

### Payment Rules:
1. **Amount Validation**: Payment amount must equal `booking.total_amount`
2. **Status Flow**: pending → processing → completed/failed (no backward transitions)
3. **Provider Integration**: Must store provider transaction ID for reconciliation

### Course Rules:
1. **Publishing**: Only published courses appear in public catalog
2. **Price**: If course has no price, it's free (or corporate-only)

### Corporate Request Rules:
1. **Status Flow**: pending → reviewing → confirmed/rejected
2. **Assignment**: Can assign trainer during review phase
3. **Quotation**: Can add quoted price before confirmation

---

## API Endpoints Structure (Conceptual)

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token
- `POST /api/auth/verify-email` - Verify email with token

### Courses
- `GET /api/courses` - List all published courses (with filters)
- `GET /api/courses/:id` - Get course details
- `POST /api/courses` - Create course (admin only)
- `PUT /api/courses/:id` - Update course (admin only)
- `DELETE /api/courses/:id` - Delete course (admin only)

### Sessions
- `GET /api/sessions` - List sessions (with filters: course_id, date, etc.)
- `GET /api/sessions/:id` - Get session details
- `GET /api/courses/:courseId/sessions` - Get sessions for a course
- `POST /api/sessions` - Create session (admin only)
- `PUT /api/sessions/:id` - Update session (admin only)
- `DELETE /api/sessions/:id` - Cancel session (admin only)

### Bookings
- `GET /api/users/:userId/bookings` - Get user's bookings
- `GET /api/bookings/:id` - Get booking details
- `POST /api/bookings` - Create booking (authenticated)
- `PUT /api/bookings/:id/cancel` - Cancel booking
- `GET /api/sessions/:sessionId/bookings` - Get bookings for a session (admin)

### Payments
- `POST /api/payments/mpesa/initiate` - Initiate M-Pesa payment
- `POST /api/payments/flutterwave/initiate` - Initiate Flutterwave payment
- `GET /api/payments/status?ref=:reference` - Check payment status
- `POST /api/payments/webhooks/mpesa` - M-Pesa webhook handler
- `POST /api/payments/webhooks/flutterwave` - Flutterwave webhook handler

### Corporate Requests
- `POST /api/corporate/requests` - Submit corporate request (public)
- `GET /api/corporate/requests` - List requests (admin only)
- `GET /api/corporate/requests/:id` - Get request details
- `PUT /api/corporate/requests/:id` - Update request status (admin)
- `DELETE /api/corporate/requests/:id` - Delete request (admin)

### Trainers
- `GET /api/trainers` - List trainers
- `GET /api/trainers/:id` - Get trainer details
- `POST /api/trainers` - Create trainer (admin)
- `PUT /api/trainers/:id` - Update trainer (admin)

### Users (Admin)
- `GET /api/users` - List users (admin)
- `GET /api/users/:id` - Get user details
- `PUT /api/users/:id` - Update user (admin or self)
- `DELETE /api/users/:id` - Deactivate user (admin)

---

## Data Validation Rules

### User Registration:
- Email: Valid email format, unique
- Password: Minimum 8 characters, must contain letters and numbers
- Name: 2-100 characters
- Phone: Valid phone format (optional)

### Booking Creation:
- `seats`: Integer, minimum 1, maximum session.seats_left
- `session_id`: Must exist and be active
- `user_id`: Must be authenticated
- Cannot create duplicate booking

### Payment Initiation:
- `booking_id`: Must exist and have payment_status = 'pending'
- `amount`: Must match booking.total_amount
- `phone` (M-Pesa): Valid Kenyan phone number format
- `email` (Flutterwave): Valid email format

### Corporate Request:
- `company_name`: Required, 2-200 characters
- `email`: Valid email format
- `phone`: Valid phone format
- `topic`: Required, 2-500 characters
- `preferred_dates`: Array of valid ISO date strings

---

## Indexing Strategy

### High-Traffic Queries:
1. **Course Catalog**: Index on `category`, `audience`, `is_published`, `is_active`
2. **Session Search**: Composite index on `(course_id, date)`, index on `status`
3. **User Bookings**: Index on `user_id`, `created_at`
4. **Payment Lookup**: Index on `payment_reference`, `provider_transaction_id`
5. **Email Lookups**: Unique index on `email` in Users and Corporate Requests

### Full-Text Search:
- Courses: `title`, `description`
- Trainers: `name`, `bio`

---

## Security Considerations

### Authentication:
- JWT tokens with expiration
- Password hashing (bcrypt/argon2)
- Email verification required
- Password reset tokens with expiration

### Authorization:
- Role-based access control (RBAC)
- User can only access their own bookings
- Admin-only endpoints protected
- Trainer can view their own courses/sessions

### Data Protection:
- Encrypt sensitive data (payment info, personal data)
- Sanitize user inputs
- Rate limiting on authentication endpoints
- CORS configuration
- SQL injection prevention (parameterized queries)

### Payment Security:
- Webhook signature verification
- Idempotency keys for payment requests
- Secure storage of provider credentials
- Audit trail for all payment transactions

---

## Scalability Considerations

### Database:
- Consider read replicas for high read traffic
- Partition large tables (e.g., payments by date)
- Archive old bookings/payments
- Use connection pooling

### Caching:
- Cache course catalog (5-10 minutes)
- Cache session availability
- Cache user sessions (JWT)
- Invalidate cache on updates

### Background Jobs:
- Email notifications (registration, booking confirmation, etc.)
- Payment status polling (if needed)
- Session reminders
- Corporate request notifications

### File Storage:
- Course images: CDN or object storage (S3, Cloudinary)
- Trainer photos: Same as above
- Use optimized image formats (WebP)

---

## Migration Strategy

### Phase 1: Core Entities
1. Users
2. Trainers
3. Courses
4. Sessions

### Phase 2: Booking System
5. Bookings
6. Payments

### Phase 3: Corporate Features
7. Corporate Requests

### Phase 4: Enhancements
8. Payment Webhooks (if needed)
9. Additional indexes based on usage patterns

---

## Notes

- All timestamps should use UTC
- Use UUIDs for primary keys (better for distributed systems)
- Soft deletes recommended for Users, Courses, Sessions (use `is_active` or `deleted_at`)
- Consider adding audit fields (`created_by`, `updated_by`) for admin operations
- Add database constraints (foreign keys, check constraints) at database level
- Use transactions for booking creation + payment initiation
- Consider adding a `notifications` table for user notifications
- Consider adding a `reviews` table for course/trainer ratings

---

## Optional Enhancements

### Reviews & Ratings:
- `Reviews` table linked to Courses and Trainers
- Rating aggregation in Courses/Trainers tables

### Waitlists:
- `Waitlists` table for fully booked sessions
- Auto-notify when seats become available

### Certificates:
- `Certificates` table for course completion certificates
- Linked to Users and Courses

### Notifications:
- `Notifications` table for in-app notifications
- Email notifications via background jobs

### Analytics:
- `Analytics` or `Events` table for tracking user behavior
- Course popularity, booking patterns, etc.

