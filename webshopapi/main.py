"""
MSPR 4 - Webshop API
"""
import json
import requests
import logging
import uvicorn
# from email.header import Header
from functools import wraps
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from urllib.parse import unquote
from database.database import Db
from utilities.token_func import encode_token, decode_token


# api mise à disposition dans le sujet
# api clients
API_CLIENT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers"
# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"
# prefixe Url
API_PREFIX = "/apiws/v1"

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

## Token

You will be able to **create / delete / update token** if you have the admin rights

- The admin will be able to **create a token** if he has the correct rights.

**description:**s
when this api is called, the token will be created and sent to db for webshop.



url: /api/v1/create-token/{token_id}/{token}

call the api with curl:
```shell
curl -X 'POST' \
    'http://localhost:82/api/v1/create-token/1/mot_de_passe' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer admin'
```

- The admin will be able to **delete a token** if he has the correct rights.

url: /api/v1/delete-token/{token_id}

call the api with curl:
```shell
curl -X 'DELETE' \
    'http://localhost:82/api/v1/delete-token/1' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer admin'
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
    },
    {
        "name": "Token",
        "description": "Manage token.",
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

db = Db('data/database', clear=False)
# db.__enter__()
db.create_tables()


@app.on_event("shutdown")
def shutdown_event():
    db.__exit__(None, None, None)


def admin_required(func):
    """
    Decorator to check if the user is admin
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token') #or Header(None)
        if not token:
            raise HTTPException(status_code=401, detail='Token is missing')
        if token.credentials != "admin":
            raise HTTPException(status_code=403, detail='You are not admin')

        return func(*args, **kwargs)

    return wrapper

def token_required(func):
    """
    Decorator to check if the token is valid
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token') #or Header(None)
        if not token:
            raise HTTPException(status_code=401, detail='Token is missing')
        token_decoded = decode_token(token.credentials)
        if token_decoded == 1:
            raise HTTPException(status_code=401, detail='Token has expired')
        elif token_decoded == 2:
            raise HTTPException(status_code=401, detail='Token is not valid')
        if db.get_token(token_decoded) is False:
            raise HTTPException(status_code=403,
                                detail='Token has been deleted and has no rights to access this resource')
        return func(*args, **kwargs)

    return wrapper


# route principale

@app.get("/")
def read_root():
    """
    Root path
    """
    return {"message": "Welcome to the MSPR API Webshop"}


# Customers routes

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


# Products routes

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

# Token routes

@app.post(f"{API_PREFIX}/create-token/{{token_id}}/{{mdp}}", tags=["Token"])
@admin_required
def create_user(token_id: int, mdp: str, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Create a Token
    :param token_id:
    :param mdp:
    :param token:
    :return:
    """
    try:
        decoded_mdp = unquote(mdp)
        token = encode_token(decoded_mdp)
        if db.insert_token(token_id, token) is False:
            return {"status": "error", "message": f"Token with id {token_id} already exists on the database"}
        return {"status": "success",
                "message": f"Token with id {token_id} has been created"}
    except Exception as e:
        return {"status": "error", "message": e.__repr__()}


@app.delete(f"{API_PREFIX}/delete-token/{{token_id}}", tags=["Token"])
@admin_required
def delete_user(token_id: int, token: Annotated[str, Depends(token_auth_scheme)]):
    """
    Delete a Token
    :param token_id:
    :param token:
    :return:
    """
    try:
        if db.delete_user(token_id) is False:
            return {"status": "error", "message": f"User with id {token_id} does not exist on the database"}
        return {"status": "success", "message": f"User with id {token_id} has been deleted"}
    except Exception as e:
        return {"status": "error", "message": e.__repr__()}


if __name__ == "__main__":
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=81, log_level="debug", access_log=True)
    # uvicorn.run(app)

