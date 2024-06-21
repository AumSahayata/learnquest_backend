from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .models import User
from .schemas import TokenData, UserCreateModel, Token
from .utils import generate_password_hash, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.config import Config
from jwt.exceptions import InvalidTokenError
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM

class UserOperations:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        
        result = await session.execute(statement)
        user = result.scalars().first()
        if user is None:
            return None
        return user
    
    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )
        
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        
        session.add(new_user)
        
        await session.commit()
        
        return new_user
    
    async def get_user_by_uid(self, uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == uid)
        
        result = await session.execute(statement)
        user = result.scalars().first()
        if user is None:
            return None
        return user
    
    async def authenticate_user(self, email: str, password: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user
    
    # async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession):
    
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
        
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    #         uid = payload.get('sub')
    #         is_instructor = payload.get('is_instructor')
    #         if(uid is None):
    #             raise credentials_exception
    #         token_data = TokenData(uid = uid, is_instructor = is_instructor)
    #     except InvalidTokenError:
    #         raise credentials_exception
    #     user = await self.get_user_by_uid(token_data.uid, session)
    #     if user is None:
    #         raise credentials_exception
    #     return user