from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import TaskPriority, TaskStatus
from app.models.models import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task_by_id(db: AsyncSession, task_id: int) -> Task:
    """Fetch a task by its ID or raise 404."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def get_tasks_by_user(
    db: AsyncSession,
    user_id: int,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    deadline_before: Optional[datetime] = None,
    deadline_after: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
    order_by: str = "created_at",
    order_dir: str = "desc",
    show_completed: bool = True,
) -> List[Task]:
    """Return all tasks for a specific user, with optional filters and sorting."""
    query = select(Task).where(Task.owner_id == user_id)

    if not show_completed:
        query = query.where(Task.status != TaskStatus.DONE)
    if status is not None:
        query = query.where(Task.status == status)
    if priority is not None:
        query = query.where(Task.priority == priority)
    if deadline_before is not None:
        query = query.where(Task.deadline <= deadline_before)
    if deadline_after is not None:
        query = query.where(Task.deadline >= deadline_after)

    if order_by not in {"created_at", "deadline"}:
        order_by = "created_at"
    order_column = getattr(Task, order_by)
    if order_dir == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


async def create_task(db: AsyncSession, task_data: TaskCreate, owner_id: int) -> Task:
    """Create a new task for a user."""
    new_task = Task(**task_data.model_dump(exclude_unset=True), owner_id=owner_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate) -> Task:
    """Update fields of an existing task."""
    task = await get_task_by_id(db, task_id)
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int):
    """Delete a task by its ID."""
    task = await get_task_by_id(db, task_id)
    await db.delete(task)
    await db.commit()


async def search_tasks(
    db: AsyncSession, owner_id: int, title: str = None, description: str = None
) -> List[Task]:
    """Search for tasks by title and/or description."""
    query = select(Task).where(Task.owner_id == owner_id)
    if title:
        query = query.where(Task.title.ilike(f"%{title}%"))
    if description:
        query = query.where(Task.description.ilike(f"%{description}%"))
    result = await db.execute(query)
    return result.scalars().all()
