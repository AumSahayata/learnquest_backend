from typing import List
from fastapi import APIRouter, Depends, Request, status, HTTPException
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

@course_router.get("/instructor", response_model = List[Course])
async def get_instructor_courses(request: Request, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user

    if user.is_instructor:
        creator_uid = user.uid
        courses = await course_operations.get_all_creator_courses(creator_uid, session)
        
        return courses
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an instructor")

@course_router.get("/{course_uid}", response_model = Course)
async def get_course(course_uid: str, session: AsyncSession = Depends(get_session)):
    course = await course_operations.get_course_by_uid(course_uid, session)
    
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not Found")
    
    return course

@course_router.get("/keywords/{keywords}", response_model=List[Course])
async def get_keyword_courses(keywords: str, session: AsyncSession = Depends(get_session)):
    courses = await course_operations.get_courses_with_keyword(keywords, session)
    
    return courses

@course_router.post("/create", response_model = Course, status_code = status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreateModel, request: Request, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user.is_instructor:
        creator_uid=user.uid
        new_course = await course_operations.create_course(creator_uid, course_data, session)
        return new_course
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only instructors can create course")

@course_router.patch("/update/{course_uid}", response_model=Course)
async def update_course(request: Request, course_uid: str, course_data: CourseUpdateModel, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user.is_instructor:
        instructor_uid=user.uid
        updated_course = await course_operations.update_course(instructor_uid, course_uid, course_data, session)

        if updated_course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        return updated_course
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only creator can update course")

@course_router.delete("/delete/{course_uid}", status_code=status.HTTP_200_OK)
async def delete_course(course_uid: str, request: Request, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user.is_instructor:
        instructor_uid = user.uid
        course_to_delete = await course_operations.delete_course(instructor_uid, course_uid, session)
        
        if course_to_delete == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        else:
            return {"detail":"Deleted successfully"}