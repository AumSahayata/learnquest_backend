from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import ContentCreateModel, ContentResponseModel, ContentUpdateModel
from .models import Content
from .operations import ContentOperations

content_router = APIRouter()

content_operations = ContentOperations()

@content_router.get("/all/{course_uid}", response_model = List[Content])
async def get_content_of_course(course_uid: str, session: AsyncSession = Depends(get_session)):
    content = await content_operations.get_content_by_course_uid(course_uid, session)
    
    if content:
        return content
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")

@content_router.get("/{content_uid}", response_model=ContentResponseModel)
async def get_content(content_uid: str, session: AsyncSession = Depends(get_session)):
    content = await content_operations.get_content_by_content_uid(content_uid, session)
    
    if content:
        return content
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")

@content_router.post("/", response_model=ContentResponseModel, status_code = status.HTTP_201_CREATED)
async def create_content(request:Request, content_data: ContentCreateModel, session: AsyncSession = Depends(get_session)):
    user = request.state.user
    
    if user.is_instructor:
        new_content = await content_operations.create_content(content_data, session)
        return new_content
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only instructors of the course can create content")

@content_router.patch("/{content_uid}", response_model=ContentResponseModel)
async def update_content(request:Request, content_uid: str, update_data: ContentUpdateModel, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user.is_instructor:
        creator_uid = user.uid
        updated_content = await content_operations.update_content(creator_uid, content_uid, update_data, session)
        
        if updated_content:
            return updated_content
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only creator can update content")
    
@content_router.delete("/{content_uid}", status_code=status.HTTP_200_OK)
async def delete_content(request:Request, content_uid: str, session: AsyncSession = Depends(get_session)):
    user = request.state.user
    
    if user.is_instructor:
        creator_uid = user.uid
        content_deleted = await content_operations.delete_content(creator_uid, content_uid, session)
        if content_deleted == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
        else:
            return {"detail":"Deleted successfully"}