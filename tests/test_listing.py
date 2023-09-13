from fastapi.testclient import TestClient
import pytest
import os
from config import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dependencies.database import Base
from dependencies.get_db import get_db


# @pytest.fixture(scope="session")
# def test_db():
#     MOCK_DATABASE_URL = "sqlite:///./test.db"
#     engine = create_engine(MOCK_DATABASE_URL)
#     sessionLocal = sessionmaker(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield sessionLocal()
#     Base.metadata.drop_all(bind=engine)
#     if os.path.exists("test_test.db"):
#         os.remove("test_test.db")

# @pytest.fixture(scope="session")
# def client(test_db):
#     app.dependency_overrides[get_db] = lambda: test_db
#     client = TestClient(app)
#     yield client

client = TestClient(app)

def test_create_list():
    _json = {
        "address": "stringgg",
        "createAt": "2023-09-12T08:30:13",
        "type": "HOUSE",
        "availableNow": True,
        "owner_id": 1,
        "updateAt": None
    }
    response = client.post("/api/listing", json=_json)
    assert response.status_code == 200
    assert response.json()["message"] == "ok"



def test_get_all_list():
    response = client.get("/api/listing")
    assert response.status_code == 200
    assert response.json()["message"] == "ok"



def test_get_one_list():
    response = client.get("/api/listing/1",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2OTQ0OTYxNzV9.NkphikEk8QuNm6B_Cc_X9WBRl4sIl1dvgXuvUmTmYe0"})
    assert response.status_code == 200
    assert response.json()["message"] == "ok"



def test_update_list():
    _json = {
        "id": 1,
        "address": "string",
        "createAt": "2023-09-12T08:30:13",
        "type": "HOUSE",
        "availableNow": True,
        "owner_id": 1,
        "updateAt": None
    }
    response = client.put("/api/listing/1", json=_json, headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2OTQ0OTYxNzV9.NkphikEk8QuNm6B_Cc_X9WBRl4sIl1dvgXuvUmTmYe0"})
    assert response.status_code == 200
    assert response.json() == "list successfully updated"
    


def test_delete_list():
    response = client.delete("/api/listing/1",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2OTQ0OTYxNzV9.NkphikEk8QuNm6B_Cc_X9WBRl4sIl1dvgXuvUmTmYe0"})
    assert response.status_code == 200
    assert response.json() == "list successfully deleted"

