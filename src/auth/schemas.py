from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    username: str = Field(max_length=15)
    email: str
    password: str = Field(min_length=6)