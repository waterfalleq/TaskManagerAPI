from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    """Shared fields for task creation and updates."""

    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Fields required to create a new task."""

    pass


class TaskUpdate(TaskBase):
    """Fields allowed for updating an existing task."""

    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Response model for tasks, including IDs and timestamps."""

    id: int
    owner_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
