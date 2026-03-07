from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from sqlalchemy.engine import Result
from src.models import User
from src.schemas import UserCreate, UserUpdate

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return await db.scalar(stmt)

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return await db.scalar(stmt)

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    result: Result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)


async def create_user(db: AsyncSession, data: UserCreate) -> User:
   
    existing_email = await get_user_by_email(db, data.email)
    if existing_email:
        raise ValueError(f"Email {data.email} already registered")
    
    existing_username = await get_user_by_username(db, data.username)
    if existing_username:
        raise ValueError(f"Username {data.username} already taken")
    
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=""
    )
    
    user.set_password(data.password)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True