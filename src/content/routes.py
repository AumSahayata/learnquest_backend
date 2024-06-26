from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import ContentCreateModel, ContentUpdateModel
from .models import Content
from .operations import ContentOperations

content_router = APIRouter()

content_operations = ContentOperations()

@content_router.get("/{course_uid}", response_model = List[Content])
async def get_content(course_uid: str, session: AsyncSession = Depends(get_session)):
    content = await content_operations.get_content_by_course_uid(course_uid, session)
    
    return content

@content_router.post("/", response_model=Content, status_code = status.HTTP_201_CREATED)
async def create_content(request:Request, content_data: ContentCreateModel, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user.is_instructor:
        new_content = await content_operations.create_content(content_data, session)
        return new_content
    
    else:
        pass

@content_router.patch("/{content_uid}", response_model = Content)
async def update_content(content_uid: str, update_data: ContentUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_content = await content_operations.update_content(content_uid, update_data, session)
    
    if updated_content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return updated_content