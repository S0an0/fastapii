from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from sqlalchemy.engine import Result
from src.models import Task
from src.schemas import CreateTask, UpdateTask


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Task]:
    stmt = select(Task).offset(skip).limit(limit)
    result: Result = await db.execute(stmt)
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    return await db.get(Task, task_id)


async def get_task_by_id(db: AsyncSession, id: str) -> Optional[Task]:
    stmt = select(Task).where(Task.id == id)
    return await db.scalar(stmt)

 
async def create_task(db: AsyncSession, data: CreateTask) -> Task:
    task = Task(**data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task_id: int, data: UpdateTask) -> Optional[Task]:

    task = await get_task(db, task_id)

    if not task:
        return None
    
    # Обновляем поля из Pydantic модели
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    task = await get_task(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True