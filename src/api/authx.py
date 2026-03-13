from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth import auth
from src.core.hashing import pwd_context
from src.database import get_session
from src.models import User
from src.schemas import AuthUser, UserResponse
from src.crud.Users import get_user_by_username

router = APIRouter(prefix="/auth", tags=["authorization"])

@router.post("/login")
async def login(
    data: AuthUser,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_username(session,data.username)

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = auth.create_access_token(uid=str(user.id))
    auth.set_access_cookies(token, response)

    return {"message": "Успешный вход", "username": user.username}


@router.post("/logout")
def logout(response: Response):
    auth.unset_access_cookies(response)
    return {"message": "Выход выполнен"}


@router.get("/me", response_model=UserResponse)
async def get_me(
    token_payload=Depends(auth.access_token_required),
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, int(token_payload.sub))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user