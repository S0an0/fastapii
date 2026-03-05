from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.TaskUserAssociation import TaskUserAssociation
from src.schemas.TaskUserAssociation import TaskUserCreate, TaskUserUpdate
from typing import List, Optional

async def create_association(
    db: AsyncSession, 
    data: TaskUserCreate
) -> TaskUserAssociation:
    association = TaskUserAssociation(**data.model_dump())
    db.add(association)
    await db.commit()
    await db.refresh(association)
    return association

async def get_user_tasks(
    db: AsyncSession, 
    user_id: int
) -> List[TaskUserAssociation]:
    result = await db.execute(
        select(TaskUserAssociation)
        .where(TaskUserAssociation.user_id == user_id)
    )
    return result.scalars().all()

async def get_task_users(
    db: AsyncSession, 
    task_id: int
) -> List[TaskUserAssociation]:
    result = await db.execute(
        select(TaskUserAssociation)
        .where(TaskUserAssociation.task_id == task_id)
    )
    return result.scalars().all()

async def delete_association(
    db: AsyncSession, 
    association_id: int
) -> bool:
    result = await db.execute(
        select(TaskUserAssociation)
        .where(TaskUserAssociation.id == association_id)
    )
    association = result.scalar_one_or_none()
    if association:
        await db.delete(association)
        await db.commit()
        return True
    return False