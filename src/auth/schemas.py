from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    email: str
    password: str = Field(min_length=6)

class UserLoginModel(BaseModel):
    email: str
    password: str = Field(min_length=6)
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    uid: str
    is_instructor: bool
    
class UserPasswordHash(UserCreateModel):
    password_hash: str
