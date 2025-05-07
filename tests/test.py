import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_reg(): #testing register function
    response = client.post("/auth/register", json={
        "username": "pytest",
        "email": "pytest@test.com",
        "password": "pytest"
    })
    assert response.status_code == 200 or response.status_code == 400 #400 if user already exists
    
