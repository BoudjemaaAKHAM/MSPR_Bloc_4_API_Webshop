from typing import Optional
from typing import Union
from typing import List

from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException, Depends

from pydantic import BaseModel

# si uvicorn  attention a commenter dans docker
import uvicorn

# import pour la connection
import sqlalchemy
from sqlalchemy import create_engine
# import mysql.connector
import pymysql


# import pour creer une table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
from sqlalchemy import DateTime
import enum
from sqlalchemy.types import Enum 
from sqlalchemy import desc
from sqlalchemy import asc

# insertion de données
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import union_all

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# json encoder
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import time


############################################
# partie ORM SQLAlchemy creation de tables #
############################################
class Connection:
    """
    Connection and Session
    """

    def __init__(self):
        self.user = 'tdi'
        self.password = 'tdi'
        self.host = 'db'
        self.port = 3306
        self.database = 'tdi'
        
    def get_connection(self):
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                self.user, self.password, self.host, self.port, self.database
            ), pool_recycle=60 * 5, pool_pre_ping=True, echo = True, echo_pool="debug"
        )

    def Session(self):
        sess = sessionmaker(bind=self.get_connection(), expire_on_commit=False)
        return sess()
    
c = Connection()
session = c.Session()

#creation d'une table
# pour approfondir les relations entre table lors de sa construction voir site:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
Base = declarative_base()

#-----------------table relation----------------------

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(30))
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# pour lancer la creation de tables avec la connection
Base.metadata.create_all(c.get_connection())

# #debut de FastAPI
app = FastAPI()

###############################
# toutes les commandes en get #
###############################

# home
@app.get("/")
async def hello_world():
    return {"hello":"world"}

# inspirer du site : https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# ou encore orienté select : https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
# read by id User_Account relation Adress.user_id == User.id
@app.get("/read_User_Account/{id}") # {id}
async def read_one_User(id: int): #id: int

    stmt1 = (select(Address.email_address)
        .select_from(User) 
        .join(Address, User.id == Address.user_id)
        .where(User.id == id)) # 
    stmt2 = (select(User)
        .where(User.id == id))

    readUserAccount = session.scalars(stmt2).all() #.all() #.one() #.first()
    readUserAccount = readUserAccount + (session.scalars(stmt1).all())
    session.commit()
    return readUserAccount


###########################
# toute les commande post #
###########################

# insert by name, fullname, emailaddress sans paramettre visible
@app.post("/createUserAcount/") # 
async def createUseraccount(name: str, fullname: str, addresses: str):
    add_user_acount = User(name = name, fullname = fullname, addresses = [Address(email_address = addresses)] )
    session.add(add_user_acount)
    session.commit()
    # time.sleep(4)
    return {"name": name,"fullname": fullname, "addresses": addresses}

##########################
# toute les commande put #
##########################

# update by id, name, fullname on UserAcount
@app.put("/updatePutUserAcount/{id}/{name}/{fullname}/{addresses}")
async def updatePutUserAcount(id: int, name: str, fullname: str, addresses: str):
    update_user_acount = (update(User)
        .where(User.id == id)
        .values(name = name, fullname = fullname))
    update_Address = (update(Address)
        .where(User.id == id)
        .where(Address.user_id == User.id)
        .values(email_address = addresses))
    session.execute(update_user_acount)
    session.execute(update_Address)
    session.commit()

    return {"Update": id,"name": name,"fullname": fullname, "address": addresses}

#############################
# toute les commande delete #
#############################

# delete by id
@app.delete("/deleteUserAcount/{id}")
async def deleteUserAcount(id: int):
    add_user = session.query(User).get(id)
    session.delete(add_user)
    session.commit()
    return {"delete": id}

##########################
# pour lancer le serveur #
##########################
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)