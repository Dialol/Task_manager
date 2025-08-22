import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post(
            "/tasks/",
            params={"name": "Тест", "description": "Описание"}
            )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тест"
    assert data["description"] == "Описание"
    assert data["status"] == "created"
    assert "id" in data

def test_get_task():
    create_response = client.post(
            "/tasks/", 
            params={"name": "Тест", "description": "Описание"}
            )
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    create_response = client.post(
            "/tasks/",
            params={"name": "Тест", "description": "Описание"}
            )
    task_id = create_response.json()["id"]
    
    response = client.put(
            f"/tasks/{task_id}", 
            params={"name": "Новое имя", "status": "in_progress"}
            )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Новое имя"
    assert data["status"] == "in_progress"

def test_delete_task():
    create_response = client.post(
            "/tasks/", 
            params={"name": "Тест", "description": "Описание"}
            )
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_task_not_found():
    response = client.get("/tasks/nonexistent")
    assert response.status_code == 404

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
