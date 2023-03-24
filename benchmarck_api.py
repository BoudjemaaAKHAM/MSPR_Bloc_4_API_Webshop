from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import requests
import json
from typing import Annotated

# api mise à disposition dans le sujet
# api clients
API_CLIENT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers"
# api produits
API_PRODUCT = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"

# Partie sécurité à tester
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

description = """
Documentation des APIs du projet MSPR 4. 🚀

## Customers

You will be able to **read customers**.

## Orders

You will be able to **read orders**.

## Products

You will be able to **read products**.

"""

tags_metadata = [
    {
        "name": "customers",
        "description": "Manage customers.",
    },
    {
        "name": "orders",
        "description": "Manage orders.",
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

# Modèle de données pour les clients
# Ce n'est pas utilisé actuellement mais l'idée serait de le faire pour client et produit


class Customer(BaseModel):
    """
    Customer model
    """
    id: int
    name: str
    ...  # etc.

# fonction pour tester la sécurité d'une api mais n'est pas testé maintenant


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# route principale


@app.get("/")
def read_root():
    """
    Root path
    """
    return {"Hello": "World"}

# routes clients


@app.get("/customers", tags=["customers"])
def get_customers():
    """
    Get all customers
    """
    response = requests.get(API_CLIENT)
    # traitement de response
    # récupération de la réponse sous forme de json
    # faire des conditions sur l'accès à l'api
    # renvoyer une erreur si l'accès n'est pas autorisé
    # renvoyer la réponse si l'accès est autorisé
    return response.json()


@app.get("/customers/{customer_id}", tags=["customers"])
def get_customer(customer_id: int):
    """
    Get a customer by id
    """

    response = requests.get(API_CLIENT + "/" + str(customer_id))
    return response.json()


@app.get("/customers/{customer_id}/orders", tags=["customers"])
def get_customer_orders(customer_id: int):
    """
    Get all orders of a customer
    """
    response = requests.get(API_CLIENT + "/" + str(customer_id) + "/orders")
    return response.json()

# routes produits


@app.get("/products", tags=["products"])
def get_products():
    """
    Get all products
    """
    response = requests.get(API_PRODUCT)
    return response.json()


@app.get("/products/{product_id}", tags=["products"])
def get_product(product_id: int):
    """
    Get a product by id
    """
    response = requests.get(API_PRODUCT + "/" + str(product_id))
    return response.json()


# post et delete pour les clients (juste pour tester) à ne pas utiliser !!!!
@app.post("/customers")
def create_customer(customer: Customer):
    response = requests.post(API_CLIENT, data=customer.json())
    return response.json()


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    response = requests.delete(API_CLIENT + "/" + str(customer_id))
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
