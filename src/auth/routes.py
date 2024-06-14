from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel
from .operations import UserOperations
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .models import User

auth_router = APIRouter()
user_operations = UserOperations()

@auth_router.post("/signup", response_model = User, status_code = status.HTTP_201_CREATED)

async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_operations.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "User with email already exists")

    new_user = await user_operations.create_user(user_data, session)

    return new_user