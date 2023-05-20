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
def token_token(client):
    db.delete_token(99)
    headers = {"Authorization": "Bearer admin"}
    response = client.post("/apiws/v1/create-token/99/test", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "success",
                               "message": "Token with id 99 has been created."}
    token_ = db.get_token(99)[2]
    return token_


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the MSPR API Webshop"}

# test customers
def test_get_customers(client, token_token):
    headers = {"Authorization":"Bearer" + token_token}
    response = client.get("/apiws/v1/customers", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == list

def test_get_customers_id(client, token_token):
    headers = {"Authorization":"Bearer" + token_token}
    response = client.get("/apiws/v1/customers/15", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_customers_id_by_orders(client, token_token):
    headers = {"Authorization":"Bearer" + token_token}
    response = client.get("/apiws/v1/customers/15/orders", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_get_customers_id_order_id_product(client, token_token):
    headers = {"Authorization":"Bearer" + token_token}
    response = client.get("/apiws/v1/customers/7/orders/7/products", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict


# test products
def test_get_products(client, token_token):
    headers = {"Authorization":"Bearer" + token_token}
    response = client.get("/apiws/v1/products", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_product_does_not_exist(client, token_token):
    headers = {"Authorization": "Bearer" + token_token}
    response = client.get("/apiws/v1/products/1", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'status': 'error', 'message': 'Product not found'}


def test_get_product_exists(client, token_token):
    headers = {"Authorization": "Bearer" + token_token}
    response = client.get("/apiws/v1/products/5", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'createdAt': '2023-02-20T01:12:28.696Z', 'name': 'Jacquelyn Hyatt',
                               'details': {'price': '662.00',
                                           'description': 'Andy shoes are designed to keeping in mind durability as well as trends, the most stylish range of shoes & sandals',
                                           'color': 'violet'}, 'stock': 67002, 'id': '5'}


def test_get_product_stock_does_not_exist(client, token_token):
    headers = {"Authorization": "Bearer" + token_token}
    response = client.get("/apiws/v1/products/1/stock", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'status': 'error', 'message': 'Product not found'}


def test_get_product_stock_exists(client, token_token):
    headers = {"Authorization": "Bearer" + token_token}
    response = client.get("/apiws/v1/products/5/stock", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == int
    assert response.json() == 67002


# test create token

def test_create_token(client):
    headers = {"Authorization": "Bearer admin"}
    response = client.post("/apiws/v1/create-token/98/test", headers=headers)
    assert response.status_code == 200
    token_ = db.get_token(98)[2]
    assert token_ == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdCIsImV4cCI6MTY4OTc3NDQ3OH0.x0FNITaFEyxqiRzJYaWAqC5Iy12MgWTr2EsG1NoPuFs"


if __name__ == '__main__':
    pytest.main(['-v'])