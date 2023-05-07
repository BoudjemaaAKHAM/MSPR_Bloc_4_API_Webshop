import pytest
from fastapi.testclient import TestClient

from webshopapi.main import app, db


# @pytest.fixture
# def db():
#    with Db(':memory:', clear=True) as db:
#        db.create_tables()
#        yield db
#    return db


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def user_token(client):
    db.delete_user(99)
    headers = {"Authorization": "Bearer admin"}
    response = client.post("/api/v1/create-user/99/test%40test.com", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "success",
                               "message": "User with id 99 has been created. Check your email for the QR code"}
    token_ = db.get_user(99)[2]
    return token_


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the MSPR API"}


# Faire les tests de l'api


if __name__ == '__main__':
    pytest.main(['-v'])
