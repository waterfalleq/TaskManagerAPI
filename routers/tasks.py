from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from auth.jwt_handler import get_current_user
from db.database import get_db
from models.models import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from crud.task_crud import (
    create_task,
    get_tasks_by_user,
    get_task_by_id,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task_handler(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, task, owner_id=current_user.id)


@router.get("/", response_model=List[TaskResponse])
def get_tasks_by_user_handler(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    tasks = get_tasks_by_user(db, current_user.id)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id_handler(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to access this task")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_handler(
    task: TaskUpdate,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_task = get_task_by_id(db, task_id)
    if existing_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this task")

    updated_task = update_task(db, task_id, task)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_handler(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this task")

    delete_task(db, task_id)
    return
