from typing import List
from fastapi import APIRouter, Depends, Request, status, HTTPException

from src.auth.utils import decode_token
from .models import Course
from .schemas import CourseCreateModel, CourseUpdateModel
from src.db.main import get_session
from .operations import CourseOperations
from sqlmodel.ext.asyncio.session import AsyncSession

course_router = APIRouter()

course_operations = CourseOperations()

@course_router.get("/", response_model = List[Course])
async def get_all_courses(page: int, limit: int = 5, session: AsyncSession = Depends(get_session)):
    
    offset = (page - 1) * limit
    
    courses = await course_operations.get_all_courses(session, offset, limit)
    
    return courses

@course_router.get("/{course_uid}", response_model = Course)
async def get_course(course_uid: str, session: AsyncSession = Depends(get_session)):
    course = await course_operations.get_course(course_uid, session)
    
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not Found")
    
    return course

@course_router.post("/", response_model = Course, status_code = status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreateModel, session: AsyncSession = Depends(get_session)):
    new_course = await course_operations.create_course(course_data, session)
    return new_course

@course_router.patch("/{course_uid}", response_model=Course)
async def update_course(course_uid: str, request: Request, course_data: CourseUpdateModel, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user  # User information from the middleware

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User information not found",
    )
    
    updated_course = await course_operations.update_course(course_uid, course_data, session)
    
    if updated_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return updated_course

@course_router.delete("/{course_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_uid: str, session: AsyncSession = Depends(get_session)):
    
    course_to_delete = await course_operations.delete_course(course_uid, session)
    
    if course_to_delete == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    else:
        return {}