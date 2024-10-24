"""
This module contains unit tests for the FastAPI application endpoints.
"""

# @Codebase

import pytest
from fastapi.testclient import TestClient
from ..app.main import app
from ..app.models.model import Response

# Create a TestClient instance
client = TestClient(app)

@pytest.mark.asyncio
async def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Message Response System"}

@pytest.mark.asyncio
async def test_greet_user():
    """Test the greet_user endpoint."""
    response = client.post("/greet_user")
    assert response.status_code == 200
    response_json = response.json()
    assert "response" in response_json
    assert isinstance(response_json["response"], str)
    assert "email" not in response_json

@pytest.mark.asyncio
async def test_select_message():
    """Test the message endpoint."""
    test_data = {
        "type": "formal",
        "user_message": "Schedule a meeting",
        "email": "test@example.com"
    }
    response = client.post("/message", json=test_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "response" in response_json
    assert "email" in response_json
    assert response_json["email"] == test_data["email"]
    assert isinstance(response_json["response"], str)

@pytest.mark.asyncio
async def test_respond_to_email():
    """Test the email_responder endpoint."""
    test_data = {
        "email_address": "sender@example.com",
        "email": "This is a test email content.",
        "prompt": "Respond politely",
        "type": "formal"
    }
    response = client.post("/email_responder", json=test_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "response" in response_json
    assert "email" in response_json
    assert response_json["email"] == test_data["email_address"]
    assert isinstance(response_json["response"], str)

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for invalid requests."""
    response = client.post("/message", json={})
    assert response.status_code == 422  # Unprocessable Entity

    response = client.post("/email_responder", json={})
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_response_model():
    """Test that responses conform to the Response model."""
    response = client.post("/greet_user")
    assert response.status_code == 200
    Response(**response.json())

    test_data = {
        "type": "casual",
        "user_message": "Hello",
        "email": "test@example.com"
    }
    response = client.post("/message", json=test_data)
    assert response.status_code == 200
    Response(**response.json())
