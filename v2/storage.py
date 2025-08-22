"""In-memory хранилище (словарь) для задач"""
from typing import Dict, List, Optional
from models import Task, Status
import uuid


class TaskStorage:
    """Простое in-memory хранилище задач"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def create_task(self, name: str, description: str) -> Task:
        """Создать новую задачу"""
        # uuid4 уникальный, при удалении следующая задача не получит такой же id
        # не угадать имея предыдущий
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=name,
            description=description,
            status=Status.CREATED
        )
        self._tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Получить задачу по ID"""
        # все просто получаем по uuid
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Получить все задачи"""
        # все values словаря
        return list(self._tasks.values())
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Обновить задачу"""
        # проверка если ли uuid,
        if task_id not in self._tasks:
            return None
        # именнованные передаем в функцию name="New name" и заменяем
        task = self._tasks[task_id]
        for field, value in kwargs.items():
            if value is not None and hasattr(task, field):
                setattr(task, field, value)
        
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Удалить задачу"""
        # проверка если есть -> удаляем
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
