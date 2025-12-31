from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.core.enums import CourseCategory, Audience

router = APIRouter()


@router.get("", response_model=List[CourseResponse])
async def list_courses(
    category: Optional[CourseCategory] = None,
    audience: Optional[Audience] = None,
    is_published: Optional[bool] = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all courses with optional filters"""
    query = db.query(Course).filter(Course.is_active == True)
    
    if is_published is not None:
        query = query.filter(Course.is_published == is_published)
    
    if category:
        query = query.filter(Course.category == category)
    
    if audience:
        query = query.filter(Course.audience == audience)
    
    courses = query.offset(skip).limit(limit).all()
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID, db: Session = Depends(get_db)):
    """Get course details"""
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.is_active == True
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new course (admin only)"""
    course = Course(**course_data.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a course (admin only)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    update_data = course_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a course (admin only) - soft delete"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course.is_active = False
    db.commit()
    return None

