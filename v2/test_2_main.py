import pytest
from fastapi.testclient import TestClient
from main import app, storage


# Тестовый клиент
client = TestClient(app)


class TestTaskCreation:
    """Тесты создания задач"""
    
    def test_create_task_success(self):
        """ПОЗИТИВНЫЙ: Успешное создание задачи"""
        # Очищаем перед тестом так как у нас просто словарь в памяти
        storage._tasks.clear() 
        # запрос
        response = client.post("/tasks/", json={
            "name": "Тестовая задача",
            "description": "Описание тестовой задачи"
        })
        # Ожидаемый ответ
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Тестовая задача"
        assert data["status"] == "created"
        assert "id" in data
    
    def test_create_task_validation(self):
        """НЕГАТИВНЫЙ: Валидация при создании задачи"""
        storage._tasks.clear()  
        
        # Пустое название
        response = client.post("/tasks/", json={
            "name": "",
            "description": "Описание"
        })
        assert response.status_code == 422
        
        # Слишком длинное название
        response = client.post("/tasks/", json={
            "name": "a" * 101,
            "description": "Описание"
        })
        assert response.status_code == 422
    
    def test_create_task_empty_description(self):
        """ПУСТОЙ: Создание с пустым описанием"""
        storage._tasks.clear()  
        
        response = client.post("/tasks/", json={
            "name": "Задача",
            "description": ""
        })
        assert response.status_code == 422


class TestTaskRetrieval:
    """Тесты получения задач"""
    
    # Конкретная задача GET /tasks/{task_id} 
    def test_get_task_success(self):
        """ПОЗИТИВНЫЙ: Успешное получение задачи"""
        storage._tasks.clear()  
        
        # Создаем задачу
        create_response = client.post("/tasks/", json={
            "name": "Задача для получения",
            "description": "Описание"
        })
        task_id = create_response.json()["id"]
        
        # Получаем задачу
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["id"] == task_id
    
    # Список задач GET /tasks/
    def test_get_tasks_with_data(self):
        """ПОЗИТИВНЫЙ: Получение списка задач с данными"""
        storage._tasks.clear()  
        
        # Создаем несколько задач
        client.post("/tasks/", json={
            "name": "Задача 1",
            "description": "Описание 1"
        })
        client.post("/tasks/", json={
            "name": "Задача 2", 
            "description": "Описание 2"
        })
        
        # Получаем все задачи
        response = client.get("/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 2

    def test_get_task_not_found(self):
        """НЕГАТИВНЫЙ: Получение несуществующей задачи"""
        storage._tasks.clear()  
        
        response = client.get("/tasks/nonexistent-id")
        assert response.status_code == 404
        assert "не найдена" in response.json()["detail"]
    
    def test_get_tasks_empty(self):
        """ПУСТОЙ: Получение пустого списка задач"""
        storage._tasks.clear()  
        
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []
    
    


class TestTaskUpdate:
    """Тесты обновления задач"""
    
    def test_update_task_success(self):
        """ПОЗИТИВНЫЙ: Успешное обновление задачи"""
        storage._tasks.clear()  
        
        # Создаем задачу
        create_response = client.post("/tasks/", json={
            "name": "Задача для обновления",
            "description": "Описание"
        })
        task_id = create_response.json()["id"]
        
        # Обновляем статус
        response = client.put(f"/tasks/{task_id}", json={
            "status": "in_progress"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
    
    def test_update_task_not_found(self):
        """НЕГАТИВНЫЙ: Обновление несуществующей задачи"""
        storage._tasks.clear()  
        
        response = client.put("/tasks/nonexistent-id", json={
            "name": "Новое имя"
        })
        assert response.status_code == 404
    
    def test_update_task_validation(self):
        """ПУСТОЙ: Валидация при обновлении (пустые/неправильные данные)"""
        storage._tasks.clear()  
        
        # Создаем задачу
        create_response = client.post("/tasks/", json={
            "name": "Задача для теста",
            "description": "Описание"
        })
        task_id = create_response.json()["id"]
        
        # Пустое имя
        response = client.put(f"/tasks/{task_id}", json={
            "name": ""
        })
        assert response.status_code == 422
        
        # неправильный статус
        response = client.put(f"/tasks/{task_id}", json={
            "status": "invalid_status"
        })
        assert response.status_code == 422


class TestTaskDeletion:
    """Тесты удаления задач"""
    
    def test_delete_task_success(self):
        """ПОЗИТИВНЫЙ: Успешное удаление задачи"""
        storage._tasks.clear()  
        
        # Создаем задачу
        create_response = client.post("/tasks/", json={
            "name": "Задача для удаления",
            "description": "Описание"
        })
        task_id = create_response.json()["id"]
        
        # Удаляем задачу
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        
        # Проверяем, что задача удалена
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self):
        """НЕГАТИВНЫЙ: Удаление несуществующей задачи"""
        storage._tasks.clear()  
        
        response = client.delete("/tasks/nonexistent-id")
        assert response.status_code == 404


class TestRootEndpoint:
    """Тесты корневого эндпоинта"""
    
    def test_root_endpoint(self):
        """ПОЗИТИВНЫЙ: Корневой эндпоинт"""
        storage._tasks.clear()  
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Task Manager API"
