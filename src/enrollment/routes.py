from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .operations import EnrollOperations

enrollment_router = APIRouter()

enroll_operations = EnrollOperations()

@enrollment_router.get("/check/{course_uid}", status_code=status.HTTP_200_OK)
async def enrollment_check(request: Request, course_uid: str, session: AsyncSession = Depends(get_session)):
    
    user = request.state.user
    
    if user:
        user_uid = user.uid
        is_user_enrollend = await enroll_operations.get_enrollment(user_uid, course_uid, session)
        
        if is_user_enrollend:
            return {"is_user_enrolled":"true"}
        else:
            return {"is_user_enrolled":"false"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@enrollment_router.post("/{course_uid}", status_code=status.HTTP_200_OK)
async def enroll_user(request: Request, course_uid: str, session: AsyncSession = Depends(get_session)):
    user = request.state.user
    
    if user:
        user_uid = user.uid
        enroll = await enroll_operations.enroll_user(user_uid, course_uid, session)
        
        if enroll == 1:
            return {"detail":"Enrolled successfully"}
        elif enroll == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already enrolled")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@enrollment_router.patch("/progress/{course_uid}/{progress}")
async def update_progress(request: Request, course_uid: str, progress: float, session: AsyncSession = Depends(get_session)):
    user = request.state.user
    
    if user:
        user_uid = user.uid
        progress = await enroll_operations.update_enrollment(user_uid, course_uid, progress, session)
        
        if progress:
            return {"detail":"Progress updated"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)