from pydantic import BaseModel

class CourseCreateModel(BaseModel):
    
    course_name: str
    course_description: str
    course_image: str
    course_price: float
    is_published: bool

class CourseUpdateModel(BaseModel):
    
    course_name: str
    course_description: str
    course_image: str
    course_price: float
    is_published: bool