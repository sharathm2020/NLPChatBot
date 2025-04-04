from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200, "Root endpoint did not return 200 OK"
    json_data = response.json()
    assert "message" in json_data, "Expected 'message' key in root response"
    assert isinstance(json_data["message"], str)

def test_chatbot_response_hello():
    payload = {"message": "hello"}
    response = client.post("/chat/", json=payload)
    assert response.status_code == 200, "Chat endpoint failed with 'hello'"
    json_data = response.json()
    assert "response" in json_data
    assert isinstance(json_data["response"], str)
    assert len(json_data["response"]) > 0

def test_chatbot_empty_message():
    payload = {"message": ""}
    response = client.post("/chat/", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()

def test_chatbot_long_input():
    payload = {"message": "hello " * 1000}
    response = client.post("/chat/", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()

def test_invalid_payload():
    response = client.post("/chat/", json={"msg": "hello"})
    assert response.status_code == 422, "Expected validation error for incorrect payload"
