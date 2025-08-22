"""Модели данных для Task Manager"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Status(str, Enum):
    """Статусы задач"""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    """Базовая модель задачи"""
    name: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    description: str = Field(..., min_length=1, max_length=1000, description="Описание задачи")


class TaskCreate(TaskBase):
    """Модель для создания задачи"""
    # просто наследуем от TaskBase
    pass


class TaskUpdate(BaseModel):
    """Модель для обновления задачи"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[Status] = None


class Task(TaskBase):
    """Полная модель задачи"""
    id: str
    status: Status = Status.CREATED
