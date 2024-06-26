from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
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
        return result.first()
    
    async def create_content(self, content_data: ContentCreateModel, session: AsyncSession):
        content_data_dict = content_data.model_dump()
        
        new_content = Content(
            **content_data_dict
        )
        
        session.add(new_content)
        await session.commit()
        return new_content
    
    async def update_content(self, content_uid: str, update_data: ContentUpdateModel, session: AsyncSession):
        content_to_update = await self.get_content_by_content_uid(content_uid, session)
        
        if content_to_update is not None:
            update_data_dict = update_data.model_dump()
            
            for k, v in update_data_dict.items():
                setattr(content_to_update, k, v)
                
            await session.commit()
            
            return content_to_update
        else:
            None
            
    async def check_creator(creator_uid: str, session: AsyncSession):
        statement = select(Content).join()