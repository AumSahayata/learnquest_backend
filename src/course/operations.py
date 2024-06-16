from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Course
from .schemas import CourseCreateModel, CourseUpdateModel


class CourseOperations:
    
    async def get_all_courses(self, session: AsyncSession, offset: int = 0, limit: int = 5):
        
        if offset == 0:
            statement = select(Course).limit(limit)
        else:
            statement = select(Course).offset(offset).limit(limit)
        
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def create_course(self, course_data: CourseCreateModel, session: AsyncSession):
        course_data_dict = course_data.model_dump()
        
        new_course = Course(
            **course_data_dict
            )
        
        session.add(new_course)
        await session.commit()
        return new_course
    
    async def get_course(self, course_uid: str, session: AsyncSession) -> Course:
        
        statement = select(Course).where(Course.course_uid == course_uid)
        result = await session.execute(statement)
        return result.scalar()
    
    async def update_course(self, course_uid: str, course_data: CourseUpdateModel, session: AsyncSession):
        course_to_update = await self.get_course(course_uid, session)
        
        if course_to_update is not None:
            update_data_dict = course_data.model_dump()
            
            for k, v in update_data_dict.items():
                setattr(course_to_update, k, v)
                
            course_to_update.updated_at = datetime.now()
                
            await session.commit()
            
            return course_to_update
        else:
            return None
        
    async def delete_course(self, course_uid: str, session: AsyncSession):
        course_to_delete = await self.get_course(course_uid, session)
        
        if course_to_delete is not None:
            
            await session.delete(course_to_delete)
            
            await session.commit()
            
        else:
            return -1