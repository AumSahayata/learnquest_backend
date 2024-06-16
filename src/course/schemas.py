import uuid
from pydantic import BaseModel

class CourseCreateModel(BaseModel):
    
    course_name: str
    course_description: str
    course_creator: str 
    course_image: str
    
class CourseUpdateModel(BaseModel):
    
    course_name: str
    course_description: str
    course_image: str