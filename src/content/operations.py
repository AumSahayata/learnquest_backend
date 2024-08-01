from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.course.models import Course
from .schemas import ContentCreateModel, ContentUpdateModel
from .models import Content

class ContentOperations:
    async def get_content_by_course_uid(self, course_uid: str, session: AsyncSession):
        statement = select(Content).where(Content.course_uid == course_uid).order_by(Content.content_order)
        
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_content_by_content_uid(self, content_uid: str, session: AsyncSession):
        statement = select(Content).where(Content.content_uid == content_uid)
        
        result = await session.execute(statement)
        return result.scalar()
    
    async def create_content(self, content_data: ContentCreateModel, session: AsyncSession):
        content_data_dict = content_data.model_dump()
        
        new_content = Content(
            **content_data_dict
        )
        
        session.add(new_content)
        await session.commit()
        return new_content
    
    async def update_content(self, creator_uid: str, content_uid: str, update_data: ContentUpdateModel, session: AsyncSession):
        
        if await self.check_creator(creator_uid, session):
        
            content_to_update = await self.get_content_by_content_uid(content_uid, session)
            
            if content_to_update is not None:
                update_data_dict = update_data.model_dump()
                
                for k, v in update_data_dict.items():
                    setattr(content_to_update, k, v)
                    
                await session.commit()
                
                return content_to_update
            else:
                return None
        else:
            return None
        
    async def delete_content(self, creator_uid: str, content_uid: str, session: AsyncSession):
        if await self.check_creator(creator_uid, session):
            
            content_to_delete = await self.get_content_by_content_uid(content_uid, session)
            
            if content_to_delete:
                
                await session.delete(content_to_delete)
                
                await session.commit()
            else:
                return -1
        else:
            return -1
    
    async def check_creator(self, creator_uid: str, session: AsyncSession) -> bool:
        statement = select(Course.course_creator).select_from(Course).join(Content, Content.course_uid == Course.course_uid)
                
        result = await session.execute(statement)
        user_uid = result.scalar()
        
        if str(user_uid) == creator_uid:
            return True
        else:
            return False