from app import __version__
from app.main import app
from fastapi.testclient import TestClient


def test_version():
    assert __version__ == '0.1.0'

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "hello"}
