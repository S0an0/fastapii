from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from src.database import get_session
from src.models.TaskUserAssociation import TaskUserAssociation
from src.schemas.TaskUserAssociation import (
    TaskUserCreate, 
    TaskUserResponse, 
    TaskUserUpdate,
    SetTask,
    SetUser
)

router = APIRouter(prefix="/task-user", tags=["Task-User связь"])


@router.post("/", response_model=TaskUserResponse,
            status_code=status.HTTP_201_CREATED, 
            summary="Создать связь задача-пользователь")
async def create_association(
    data: TaskUserCreate,
    db: AsyncSession = Depends(get_session)
):
    # Проверяем, существует ли уже такая связь
    existing = await db.execute(
        select(TaskUserAssociation)
        .where(
            TaskUserAssociation.task_id == data.task_id,
            TaskUserAssociation.user_id == data.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эта связь пользователь-задача уже существует"
        )
    
    association = TaskUserAssociation(**data.model_dump())
    db.add(association)
    await db.commit()
    await db.refresh(association)
    return association

@router.get("/", 
            response_model=List[TaskUserResponse],
            summary="Все связи")
async def get_all_associations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(TaskUserAssociation)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/{association_id}",
            response_model=TaskUserResponse,
            summary="Получить связь по ID")
async def get_association(
    association_id: int,
    db: AsyncSession = Depends(get_session)
):
    association = await db.get(TaskUserAssociation, association_id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Связь с ID {association_id} не найдена"
        )
    return association

@router.put("/{association_id}", 
            response_model=TaskUserResponse,
            summary="Обновить связь полностью")
async def update_association(
    association_id: int,
    data: TaskUserUpdate,
    db: AsyncSession = Depends(get_session)
):
    association = await db.get(TaskUserAssociation, association_id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Связь с ID {association_id} не найдена"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(association, field, value)
    
    await db.commit()
    await db.refresh(association)
    return association


@router.delete("/{association_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить связь оп ID связи")
async def delete_association(
    association_id: int,
    db: AsyncSession = Depends(get_session)
):
    association = await db.get(TaskUserAssociation, association_id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Связь с ID {association_id} не найдена"
        )
    
    await db.delete(association)
    await db.commit()


@router.get("/by-task/{task_id}", 
            response_model=List[TaskUserResponse],
            summary="Получить связи по задаче")
async def get_associations_by_task(
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(TaskUserAssociation)
        .where(TaskUserAssociation.task_id == task_id)
    )
    return result.scalars().all()

@router.get("/by-user/{user_id}", 
            response_model=List[TaskUserResponse],
            summary="Получить связи по пользователю")
async def get_associations_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(TaskUserAssociation)
        .where(TaskUserAssociation.user_id == user_id)
    )
    return result.scalars().all()


@router.post("/assign-task", 
            response_model=TaskUserResponse,
            summary="Назначить задачу пользователю")
async def assign_task_to_user(
    data: SetTask,
    user_id: int,  # можно передать в query параметре
    db: AsyncSession = Depends(get_session)
):
    # Проверяем существование связи
    existing = await db.execute(
        select(TaskUserAssociation)
        .where(
            TaskUserAssociation.task_id == data.task_id,
            TaskUserAssociation.user_id == user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эта задача уже назначена этому пользователю"
        )
    
    association = TaskUserAssociation(
        task_id=data.task_id,
        user_id=user_id
    )
    db.add(association)
    await db.commit()
    await db.refresh(association)
    return association

@router.post("/assign-user", 
            response_model=TaskUserResponse,
            summary = "Назначить пользователя задаче")
async def assign_user_to_task(
    data: SetUser,
    task_id: int,  # в query параметре
    db: AsyncSession = Depends(get_session)
):
    existing = await db.execute(
        select(TaskUserAssociation)
        .where(
            TaskUserAssociation.task_id == task_id,
            TaskUserAssociation.user_id == data.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже назначен этой задаче"
        )
    
    association = TaskUserAssociation(
        task_id=task_id,
        user_id=data.user_id
    )
    db.add(association)
    await db.commit()
    await db.refresh(association)
    return association

@router.delete("/unassign",
               summary = "Удалить связь")
async def unassign_task_from_user(
    task_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(TaskUserAssociation)
        .where(
            TaskUserAssociation.task_id == task_id,
            TaskUserAssociation.user_id == user_id
        )
    )
    association = result.scalar_one_or_none()
    
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Связь не найдена"
        )
    
    await db.delete(association)
    await db.commit()
    
    return {"message": "Задача успешно отменена для пользователя"}

@router.get("/check",
            summary="Проверить, существует ли связь")
async def check_association_exists(
    task_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(TaskUserAssociation)
        .where(
            TaskUserAssociation.task_id == task_id,
            TaskUserAssociation.user_id == user_id
        )
    )
    exists = result.scalar_one_or_none() is not None
    
    return {
        "task_id": task_id,
        "user_id": user_id,
        "exists": exists
    }

@router.delete("/by-task/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить все связи для задачи")
async def delete_all_task_associations(
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    await db.execute(
        delete(TaskUserAssociation)
        .where(TaskUserAssociation.task_id == task_id)
    )
    await db.commit()

@router.delete("/by-user/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить все связи для пользователя")
async def delete_all_user_associations(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    await db.execute(
        delete(TaskUserAssociation)
        .where(TaskUserAssociation.user_id == user_id)
    )
    await db.commit()