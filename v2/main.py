"""Task Manager - основное приложение FastAPI"""
from fastapi import FastAPI, HTTPException
from models import Task, TaskCreate, TaskUpdate
from storage import TaskStorage
from typing import List


app = FastAPI(
    title="Task Manager",
    description="Менеджер задач"
)

# Инициализация хранилища
storage = TaskStorage()


@app.post("/tasks/", response_model=Task, summary="Создать задачу")
def create_task(task: TaskCreate):
    """Создать новую задачу"""
    return storage.create_task(task.name, task.description)


@app.get("/tasks/{task_id}", response_model=Task, summary="Получить задачу")
def get_task(task_id: str):
    """Получить задачу по ID"""
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.get("/tasks/", response_model=List[Task], summary="Получить все задачи")
def get_tasks():
    """Получить список всех задач"""
    return storage.get_all_tasks()


@app.put("/tasks/{task_id}", response_model=Task, summary="Обновить задачу")
def update_task(task_id: str, task_update: TaskUpdate):
    """Обновить задачу"""
    update_data = task_update.model_dump(exclude_unset=True)
    task = storage.update_task(task_id, **update_data)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.delete("/tasks/{task_id}", summary="Удалить задачу")
def delete_task(task_id: str):
    """Удалить задачу"""
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}


@app.get("/", summary="Корневой эндпоинт")
def root():
    """Корневой эндпоинт"""
    return {"message": "Task Manager"}
