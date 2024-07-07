from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Enrollment

class EnrollOperations:
    
    async def enroll_user(self, user_uid: str, course_uid: str, session: AsyncSession):
        
        if not await self.get_enrollment(user_uid, course_uid, session):
        
            new_enrollment = Enrollment()
            
            new_enrollment.user_uid = user_uid
            new_enrollment.course_uid = course_uid
            
            session.add(new_enrollment)
            await session.commit()
            return 1
        else:
            
            return 0
    
    async def get_enrollment(self, user_uid: str, course_uid: str, session: AsyncSession):
        
        statement = select(Enrollment).where(Enrollment.user_uid == user_uid, Enrollment.course_uid == course_uid)
        
        result = await session.execute(statement)
        
        return result.scalar()
    
    async def update_enrollment(self, user_uid: str, course_uid: str, progress: float, session: AsyncSession):
        
        progress_to_update = await self.get_enrollment(user_uid, course_uid, session)
        
        if progress_to_update:
            progress_to_update.progress = progress
            
            await session.commit()
                
            return progress_to_update
        else:
            return None