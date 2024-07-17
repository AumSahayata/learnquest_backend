from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.content.models import Content
from src.enrollment.models import Enrollment
from .models import Course
from .schemas import CourseCreateModel, CourseUpdateModel


class CourseOperations:
    
    async def get_all_courses(self, session: AsyncSession, offset: int = 0, limit: int = 5):
        
        if offset == 0:
            statement = select(Course).where(Course.is_published == True).limit(limit)
        else:
            statement = select(Course).where(Course.is_published == True).offset(offset).limit(limit)
        
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def create_course(self, creator_uid: str, course_data: CourseCreateModel, session: AsyncSession):
        course_data_dict = course_data.model_dump()
        
        new_course = Course(
            **course_data_dict
            )
        
        new_course.course_creator = creator_uid
        
        session.add(new_course)
        await session.commit()
        return new_course
    
    async def get_course_by_uid(self, course_uid: str, session: AsyncSession) -> Course:
        
        statement = select(Course).where(Course.course_uid == course_uid, Course.is_published == True)
        result = await session.execute(statement)
        return result.scalar()
    
    async def get_creator_course_by_uid(self, course_uid: str, creator_uid: str, session: AsyncSession) -> Course:
        
        statement = select(Course).where(Course.course_uid == course_uid, Course.course_creator == creator_uid)
        result = await session.execute(statement)
        return result.scalar()
    
    async def get_course(self, course_uid: str, session: AsyncSession) -> Course:
        statement = select(Course).where(Course.course_uid == course_uid)
        result = await session.execute(statement)
        return result.scalar()
    
    async def get_all_creator_courses(self, creator_uid: str, session: AsyncSession):
        
        statement = select(Course).where(Course.course_creator == creator_uid)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_courses_with_keyword(self, keywords: str, session: AsyncSession):
        statement = select(Course).where(Course.course_name.ilike(f"%{keywords}%"), Course.is_published == True)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def update_course(self, instructor_uid: str, course_uid: str, course_data: CourseUpdateModel, session: AsyncSession):
        course_to_update = await self.get_course(course_uid, session)
        
        if course_to_update is not None and str(course_to_update.course_creator) == instructor_uid:
            update_data_dict = course_data.model_dump()
            
            for k, v in update_data_dict.items():
                setattr(course_to_update, k, v)
                
            course_to_update.updated_at = datetime.now()
                
            await session.commit()
            
            return course_to_update
        else:
            return None
        
    async def delete_course(self, instructor_uid: str, course_uid: str, session: AsyncSession):
        course_to_delete = await self.get_course(course_uid, session)
        
        if course_to_delete is not None and str(course_to_delete.course_creator) == instructor_uid:
            
            await self.delete_content_of_course(course_uid, session)
            
            await self.delete_enrollment_of_course(course_uid, session)
            
            await session.delete(course_to_delete)
            
            await session.commit()
            
        else:
            return -1
    
    async def delete_content_of_course(self, course_uid: str, session: AsyncSession):
        
        statement = select(Content).where(Content.course_uid==course_uid)
        result = await session.execute(statement)
        
        for content in result.scalars().all():
            await session.delete(content)
    
    async def delete_enrollment_of_course(self, course_uid: str, session: AsyncSession):
        
        statement = select(Enrollment).where(Enrollment.course_uid==course_uid)
        result = await session.execute(statement)
        
        for content in result.scalars().all():
            await session.delete(content)