from starlette.testclient import TestClient
from app import app

client = TestClient(app)

# Unit Testing 

def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello world again"}

def test_get_users_endpoint():
    resp = client.get("/users/22")
    assert resp.status_code == 200
    assert resp.json() == {"user_id": "22"}

def test_correct_item_post():
    json_blob = {"name": "MacBook Pro", "price": 150000}
    resp = client.post("/items/", json=json_blob)
    assert resp.status_code == 200

def test_incorrect_item_post():
    json_blob = {"name": "MacBook Air", "price": -150000}
    resp = client.post("/items/", json=json_blob)
    assert resp.status_code != 200