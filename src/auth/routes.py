from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from src.config import Config
from .schemas import UserCreateModel, Token, UserLoginModel
from .operations import UserOperations
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .models import User
from .utils import create_access_token

auth_router = APIRouter()
user_operations = UserOperations()


@auth_router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_operations.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_operations.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_for_access_token(
    user: UserLoginModel, 
    session: AsyncSession = Depends(get_session)
    ) -> Token:
    user_in_db = await user_operations.authenticate_user(user.email, user.password, session)

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(days=Config.ACCESS_TOKEN_EXPIRE_DAYS)
    data={"sub": str(user_in_db.uid), "is_instructor": user_in_db.is_instructor}
    access_token = create_access_token(data = data, exp_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

# @auth_router.post("/me", status_code=status.HTTP_200_OK)
# async def check_me(
#     token: Token,
#     session: AsyncSession = Depends(get_session)
# ) -> User:
#     user = await user_operations.get_current_user(token.access_token, session)
#     return user