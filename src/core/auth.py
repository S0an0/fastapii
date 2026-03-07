from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.database import get_session
from src.models import User
from .hashing import pwd_context
from src.crud.Users  import get_user ,get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/jwt")

async def get_token_from_cookie(request: Request) -> Optional[str]:
    """Получение токена из куки"""
    token = request.cookies.get("access_token")
    return token

async def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> Optional[str]:
    """Получение токена из заголовка"""
    return authorization



async def get_current_user(
    request: Request,
    token_from_header: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
):
    """Получение текущего пользователя (из куки или заголовка)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("ahaasdfhjasljdkhaslkdjhfalskjhfj99999999999999999999")
    
    # Сначала пробуем получить токен из куки
    token = await get_token_from_cookie(request)
    
    # Если нет в куки, пробуем из заголовка
    if not token:
        token = token_from_header
    
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            logger.warning("No username in token")
            raise credentials_exception
            
        
    except JWTError as e:
        raise credentials_exception
    
    # Получаем пользователя из БД
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    """Проверка активности пользователя"""
    # Если есть поле is_active, проверяем его
    if hasattr(current_user, 'is_active') and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Неактивный пользователь"
        )
    return current_user

async def get_user_by_username(db: AsyncSession, username: str):
    """Получение пользователя по username"""
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def verify_password(plain_password, hashed_password):
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str,db: AsyncSession = Depends(get_session)) -> Optional[User]:
    """Аутентификация пользователя"""
    stmt = await db.execute(
        select(User).where(User.username == username)
    )
    user = stmt.scalar_one_or_none()
    
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создание JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Проверка активности пользователя"""
    # Здесь можно добавить дополнительную логику, например, проверку is_active
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user