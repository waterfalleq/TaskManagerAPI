from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud.user_crud import get_user_by_id
from models.models import Task
from schemas.task import TaskCreate, TaskUpdate


def get_task_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def get_tasks_by_user(db: Session, user_id: int) -> List[Task]:
    return db.query(Task).filter(Task.owner_id == user_id).all()


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    new_task = Task(**task_data.model_dump(exclude_unset=True), owner_id=owner_id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    old_task = get_task_by_id(db, task_id)
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(old_task, key, value)
    db.commit()
    db.refresh(old_task)
    return old_task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()
