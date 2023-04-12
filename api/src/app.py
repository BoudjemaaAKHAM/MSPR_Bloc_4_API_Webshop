# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# import json
# import uvicorn

# # #debut de FastAPI
# app = FastAPI()

# ###############################
# # toutes les commandes en get #
# ###############################

# # home
# @app.get("/hello")
# async def hello_world():
#     print("hello print")
#     return  {"hello":"world"} # print("hello world")

# ##########################
# # pour lancer le serveur #
# ##########################
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9001) #"127.0.0.1"
import uvicorn

from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/read")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
 
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# ##########################
# # pour lancer le serveur #
# ##########################
#if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=3001) #"127.0.0.1"
 