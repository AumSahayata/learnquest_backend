from datetime import datetime
import uuid
from pydantic import BaseModel

class ContentCreateModel(BaseModel):
    
    course_uid: str
    content_title: str
    content_description: str
    content_type: str
    content_data: str
    content_order: int
    
class ContentUpdateModel(BaseModel):
    
    content_title: str
    content_description: str
    content_type: str
    content_data: str
    content_order: int
    
class ContentResponseModel(BaseModel):
    
    course_uid: uuid.UUID
    content_title: str
    content_description: str
    content_type: str
    content_data: str
    content_order: int
    created_at: datetime