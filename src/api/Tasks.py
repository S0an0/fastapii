from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas import CreateTask, UpdateTask 
import src.crud.Tasks as crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/" , status_code=status.HTTP_201_CREATED)
async def create_task(
    data: CreateTask, 
    db: AsyncSession = Depends(get_session)
):
    try:
        return await crud.create_task(db, data) 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}")
async def get_task(
    task_id: int, 
    db: AsyncSession = Depends(get_session)
):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

@router.get("/")
async def get_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_session)
):
    return await crud.get_tasks(db, skip=skip, limit=limit)

@router.patch("/{task_id}")
async def update_task(
    task_id: int, 
    data: UpdateTask, 
    db: AsyncSession = Depends(get_session)
):
    task = await crud.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, 
    db: AsyncSession = Depends(get_session)
):
    deleted = await crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="taks not found")