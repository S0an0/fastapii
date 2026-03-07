from fastapi import APIRouter, Response
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pydantic import BaseModel
import os
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from  src.schemas.Token import Token
from src.core.auth  import authenticate_user,create_access_token,get_current_active_user
from src.schemas.Users import UserResponse,AuthUser
from src.models.Users import User
from src.core.config import settings

router = APIRouter(prefix="/login", tags=["autorization"])

@router.post("/auth")
async def login(
    response: Response,
    form_data: AuthUser,
    db: AsyncSession = Depends(get_session)
):
    """
    Авторизация пользователя и получение токена.
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
    
    # Создаем токен
    access_token = await create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=10)
    )
    
    # Устанавливаем куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60000,
        path="/",
    )
    
    print(f"Cookie set with token: {access_token[:20]}...")  # отладка
    
    return {
        "success": True,
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@router.get("/jwt", response_model=UserResponse)
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    print("ahaasskjhfj99999999999999999999")
    """
    Пример защищенного маршрута.
    Доступен только с валидным токеном.
    """
    return current_user

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Информация о текущем пользователе"""
    return current_user


