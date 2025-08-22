from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from enum import Enum


app = FastAPI(title="Task Manager")


class Status(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress" 
    DONE = "done"


class Task(BaseModel):
    id: str
    name: str
    description: str
    status: Status


tasks_db = {}


@app.post("/tasks/", response_model=Task)
def create_task(name: str, description: str):
    task_id = str(uuid.uuid4())
    task = Task(
        id=task_id,
        name=name,
        description=description,
        status=Status.CREATED
    )
    tasks_db[task_id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Задача не найднeа")
    return tasks_db[task_id]


@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return list(tasks_db.values())


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
        task_id: str, 
        name: str = None, 
        description: str = None, 
        status: Status = None
        ):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task = tasks_db[task_id]
    if name:
        task.name = name
    if description:
        task.description = description
    if status:
        task.status = status
    
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="адач не найдена")
    del tasks_db[task_id]
    return {"message": "Задача удалена"}


@app.get("/")
def root():
    return {"message": "Task Manager API"}
