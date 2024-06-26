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