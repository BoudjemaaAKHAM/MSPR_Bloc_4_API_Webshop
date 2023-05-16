"""
MSPR 4 - Webshop API
"""
import json
import requests
import logging
import uvicorn
from functools import wraps
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.security import HTTPBearer

# api mise à disposition dans le sujet
# api clients
API_CLIENT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers"
# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"

API_PREFIX = "/apiws/v1"

# Partie sécurité à tester
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Partie sécurité
token_auth_scheme = HTTPBearer()

description = """
Documentation des APIs du projet MSPR 4. 🚀

## Customers

- The user will be able to **read customers** if he has a valid token.

url: /apiws/v1/customers

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:81/apiws/v1/customers' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```

- The user will be able to **read customers by id** if he has a valid token.

url: /apiws/v1/customers/{customer_id}

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:81/apiws/v1/customers/7' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```


- The user will be able to **read customers by id by commands orders** if he has a valid token.

url: /apiws/v1/customers/{customer_id}/orders

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:81/apiws/v1/customers/7/orders' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```

- The user will be able to **read customers by id link to id of product** if he has a valid token.

url: /apiws/v1/customers/{customer_id}/orders/{order_id}/products

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:81/apiws/v1/customers/7/orders/7/products' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```


## Products

- The user will be able to **read products** if he has a valid token.

url: /apiws/v1/products

call the api with curl:
```shell
curl -X 'GET' \
  'http://localhost:81/apiws/v1/products' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer put_token_here'
```

- The user will be able to get a **product by id** if he has a valid token.

url: /apiws/v1/products/{product_id}

call the api with curl:
```shell
curl -X 'GET' \
    'http://localhost:81/apiws/v1/products/7' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer put_token_here'
```

- The user will be able to get a **product stock by id** if he has a valid token.

url: /apiws/v1/products/{product_id}/stock

call the api with curl:
```shell
curl -X 'GET' \
    'http://localhost:81/apiws/v1/products/7/stock' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer put_token_here'
```

"""

tags_metadata = [
    {
        "name": "customers",
        "description": "Manage customers.",
    },
    {
        "name": "products",
        "description": "Manage products.",
    }
]

app = FastAPI(
    title="MSPR Bloc 4",
    description=description,
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "src": "./LICENSE.txt",
    },
    openapi_tags=tags_metadata
)


# token
def token_required(func):
    """
    Decorator to check if the user is admin
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token')  # or Header(None)
        if not token:
            raise HTTPException(status_code=401, detail='Token is missing')
        if token.credentials != "admin":
            raise HTTPException(status_code=403, detail='You are not admin')

        return func(*args, **kwargs)

    return wrapper


# route principale

@app.get("/")
def read_root():
    """
    Root path
    """
    return {"message": "Welcome to the MSPR API Webshop"}


# routes clients

@app.get(f"{API_PREFIX}/customers", tags=["customers"])
@token_required
def get_customers(token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get all customers
    :param token:
    :return: json response
    """
    response = requests.get(API_CLIENT)
    print(type(response.json()))
    if type(response.json()) == dict:
        return response.json()
    if type(response.json()) == list:
        return response.json()
    else:
        return {"status": "error", "message": "Custommer not found"}


@app.get(f"{API_PREFIX}/customers/{{customer_id}}", tags=["customers"])
@token_required
def get_customer(customer_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a customer by id
    :param customer_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_CLIENT + "/" + str(customer_id))
    if type(response.json()) == dict:
        return response.json()
    if type(response.json()) == list:
        return response.json()
    else:
        return {"status": "error", "message": "Custommer not found"}

    
@app.get(f"{API_PREFIX}/customers/{{customer_id}}/orders", tags=["customers"])
@token_required
def get_customer(customer_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a customer by id by commands orders
    :param customer_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_CLIENT + "/" + str(customer_id) + "/orders")

    if type(response.json()) == dict:
        return response.json()
    if type(response.json()) == list:
        return response.json()
    else:
        return {"status": "error", "message": "Custommer not found"}


@app.get(f"{API_PREFIX}/customers/{{customer_id}}/orders/{{order_id}}/products", tags=["customers"])
@token_required
def get_customer(customer_id: int, order_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a customer by id and product by product id and detail product
    :param customer_id:
    :param order_id:
    :param token:
    :return: json response
    """
    response1 = requests.get(API_CLIENT + "/" + str(customer_id))
    response = requests.get(API_PRODUCT + "/" + str(order_id))
    if type(response.json()) == dict and type(response1.json()) == dict:
        return response1.json()["name"], response1.json()["id"], response.json()["details"], response.json()["stock"], response.json()["id"]
    else:
        return {"status": "error", "message": "Custommer not found"}


# routes produits

# La liste des produits issue de l’ERP est accessible via l’API REST : /products.
@app.get(f"{API_PREFIX}/products", tags=["products"])
@token_required
def get_products(token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get all products
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT)
    return response.json()


# Le détail d’un produit peut être accessible via l’API REST : /products/<product id>
@app.get(f"{API_PREFIX}/products/{{product_id}}", tags=["products"])
@token_required
def get_product(product_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a product by id
    :param product_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    if type(response.json()) == dict:
        return response.json()
    else:
        return {"status": "error", "message": "Product not found"}


# l'etat des stock par produit
@app.get(f"{API_PREFIX}/products/{{product_id}}/stock", tags=["products"])
@token_required
def get_product_stock(product_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Get a product stock by id
    :param product_id:
    :param token:
    :return: json response
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    if type(response.json()) == dict:
        return response.json()["stock"]
    else:
        return {"status": "error", "message": "Product not found"}


if __name__ == "__main__":
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=81, log_level="debug", access_log=True)
    # uvicorn.run(app)

