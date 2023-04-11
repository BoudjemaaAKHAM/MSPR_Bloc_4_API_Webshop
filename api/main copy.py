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

class students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    lastname = Column(String(30))

class Usr(Base):
    __tablename__ = "usr"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(30))

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

#-----------------table projet----------------------

class Outputs(Base):
    __tablename__ = "outputs"
    date = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True)
    producer = Column(String(30))
    types = Column(Enum('txt', 'laz', 'potree'))
    path = Column(String(200))
    size = Column(Integer)
    reqestId = relationship("ReqOuputs", back_populates="output", cascade="all, delete-orphan")
    def __repr__(self):
        return f"Outputs(date={self.date!r}, id={self.id!r}, producer={self.producer!r}, types={self.types!r}, path={self.path!r}, size={self.size!r})"


# class Outputs(Base): #TAF a rentrée dans la table : date, id en liaison avec request.output, producer, type, path, size
#     __tablename__ = "outputs"
#     date = Column(DateTime, default=datetime.datetime.utcnow)
#     id = Column(Integer, primary_key=True)
#     producer = Column(String(30))
#     types = Column(Enum('txt', 'laz', 'potree'))
#     path = Column(String(200))
#     size = Column(Integer)
#     reqId = relationship("ReqOuputs", back_populates="output", cascade="all, delete-orphan")
#     def __repr__(self):
#         return f"Outputs(date={self.date!r}, id={self.id!r}, producer={self.producer!r}, types={self.types!r}, path={self.path!r}, size={self.size!r})"

class ReqOuputs(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
    __tablename__ = "reqouputs"
    id = Column(Integer, primary_key=True)
    reqid = Column(Integer, nullable=False)
    outid = Column(Integer, ForeignKey("outputs.id"), nullable=False)   #, ForeignKey("outputs.id"), nullable=False
    output = relationship("Outputs", back_populates="reqestId")
    def __repr__(self):
        return f"Address(id={self.id!r}, reqid={self.reqid!r})"

# class ReqOuputs(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
#     __tablename__ = "reqouputs"
#     id = Column(Integer, primary_key=True)
#     reqid = Column(Integer)
#     outid = Column(Integer, ForeignKey("outputs.id"), nullable=False)   #, ForeignKey("outputs.id"), nullable=False
#     output = relationship("Outputs", back_populates="reqId")
#     def __repr__(self):
#         return f"Address(id={self.id!r}, reqid={self.reqid!r})"


class Request(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
    __tablename__ = "request"
    date = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    service = Column(String(30))
    input = Column(String(500))
    statuts = Column(Enum('Succes', 'In progress', 'Error'))
    step = Column(Integer)
    # output = relationship("Output", back_populates="request")
    # output = relationship("Output", back_populates="request", cascade="all, delete-orphan")
    # def __repr__(self):
    #     return f"Request(date={self.date!r}, id={self.id!r}, userid={self.userid!r}, service={self.service!r}, input={self.input!r}, statuts={self.statuts!r}, step={self.step!r},)"

  





#-----------tentative de table intermediaire-------------

# class Outputs(Base): #TAF a rentrée dans la table : date, id en liaison avec request.output, producer, type, path, size
#     __tablename__ = "outputs"
#     date = Column(DateTime, default=datetime.datetime.utcnow)
#     id = Column(Integer, primary_key=True)
#     producer = Column(String(30))
#     types = Column(Enum('txt', 'laz', 'potree'))
#     path = Column(String(200))
#     size = Column(Integer)
#     reqId = relationship("ReqOuputs", back_populates="output", cascade="all, delete-orphan")
#     def __repr__(self):
#         return f"Outputs(date={self.date!r}, id={self.id!r}, producer={self.producer!r}, types={self.types!r}, path={self.path!r}, size={self.size!r})"
    

# class ReqOuputs(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
#     __tablename__ = "reqouputs"
#     id = Column(Integer, primary_key=True)
#     reqid = Column(Integer)
#     outid = Column(Integer, ForeignKey("outputs.id"), nullable=False)   #, ForeignKey("outputs.id"), nullable=False
#     output = relationship("Outputs", back_populates="reqId")
#     def __repr__(self):
#         return f"Address(id={self.id!r}, reqid={self.reqid!r})"


# class Request(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
#     __tablename__ = "request"
#     date = Column(DateTime, default=datetime.datetime.utcnow)
#     id = Column(Integer, primary_key=True)
#     userid = Column(Integer)
#     service = Column(String(30))
#     input = Column(String(500))
#     statuts = Column(Enum('Succes', 'In progress', 'Error'))
#     step = Column(Integer)
#     # output = relationship("Output", back_populates="request")
#     # output = relationship("Output", back_populates="request", cascade="all, delete-orphan")
#     # def __repr__(self):
#     #     return f"Request(date={self.date!r}, id={self.id!r}, userid={self.userid!r}, service={self.service!r}, input={self.input!r}, statuts={self.statuts!r}, step={self.step!r},)"


#-----------tentative de table intermediaire-------------
class Association(Base):
    __tablename__ = "association_table"
    left_id: Mapped[int] = mapped_column(Integer, ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(Integer, ForeignKey("right_table.id"), primary_key=True)
    # extra_data: Mapped[Optional[str]]
    extra_data: Mapped[Optional[int]]
    child: Mapped["Child"] = relationship()


class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    children: Mapped[List["Association"]] = relationship()


class Child(Base):
    __tablename__ = "right_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)



#--------------------------------------------------------

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

# read all de la bdd
@app.get("/read/")
async def read_all():
    todo = session.query(Usr).all() #.one()  #.all()  #.first()
    print(todo)
    readUserAccount = session.query(User).all()
    print(readUserAccount)
    readAdresse = session.query(Address).all()
    print(readUserAccount)
    session.commit()
    return "table usr", todo, "table useracount et adresse", readUserAccount, readAdresse

# read by id
@app.get("/read/{id}")
async def read_one(id: int):
    todo = session.query(Usr).get(id)
    print(todo)
    session.commit()
    # close.session()
    return todo

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

#----------------------------------------------------------------------------------------------
# -version pour l'API Ocirn Communication de Mnt-diff qui questionne l'API pour ces informations
@app.get("/api/v1.0/queue/{service}") # {id} besoin de savoir quel micro service demande
async def readStepRequest(service): #id: int service: str
    # print("ok ça marche")
    # return {'ok ça marche'}

    # get_request_step_to_do = select(Request.step, Request.date).where(Request.service == service) #.where(Request.date == LaDatePlusAncienne) # 'mnt-diff'
    # print(get_request_step_to_do)
    # reader = session.scalars(get_request_step_to_do).all()

    get_request_step_to_do = select(Request).where(Request.service == service).where(Request.step == 0).order_by(asc(Request.date)) #.where(Request.date == LaDatePlusAncienne) # 'mnt-diff'
    print(get_request_step_to_do)
    reader = session.scalars(get_request_step_to_do).all()

    # ordre de date premiere date, ordre de commencer pas commencer
    
    # +readStep =    if get_request_step_to_do == 0:
    #                                         get_request_parameter = (select(request.input))
    #                     if get_request_step_to_do == 10:
    #                                                             get_request_parameter = null
    return reader
#--------------------------------------------------------------------------------------------


###########################
# toute les commande post #
###########################

# insert automatique
@app.post("/createUser/") 
async def create_item(): 
    add_user = Usr(name = "joe",
        fullname = 'black')
    session.add(add_user)
    session.commit()  
    return {"entrée des donnée Insert en post"}

# insert by name, fullname
@app.post("/createUser/{name}/{fullname}") 
async def createUser(name: str, fullname: str):
    add_user = Usr(name = name, fullname = fullname)
    session.add(add_user)
    session.commit()
    return {"entrée des donnée Insert: name": name,"fullname": fullname}

# inspirer du site : https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# insert by name, fullname, emailaddress
@app.post("/createUserAcount/{name}/{fullname}/{addresses}") # 
async def createUseraccount(name: str, fullname: str, addresses: str): # 
    add_user_acount = User(name = name, fullname = fullname, addresses = [Address(email_address = addresses)] )
    session.add(add_user_acount)
    session.commit()
    # time.sleep(4)
    return {"name": name,"fullname": fullname, "addresses": addresses}

# insert by name, fullname, emailaddress sans paramettre visible
@app.post("/createUserAcount/") # 
async def createUseraccount(name: str, fullname: str, addresses: str):
    add_user_acount = User(name = name, fullname = fullname, addresses = [Address(email_address = addresses)] )
    session.add(add_user_acount)
    session.commit()
    # time.sleep(4)
    return {"name": name,"fullname": fullname, "addresses": addresses}
# ---------------------------------------version pour l'API------------------------------------------------------
# # version communication de rimnatt fait un premier post vers l'API (basique)

# @app.post("/api/v1.0/queue/")
# async def createServiceRequest(userid: int, service: str, input: str, statuts: str, step: int): # 
#     add_request = Request(userid = userid, service = service, input = input, statuts = statuts, step = step )
#     session.add(add_request)
#     session.commit()
#     result = session.commit()
#     print(result)
#     # a deiscuter avec loic pour le get dans le post
#     get_request_id = (select(Request.id).where(Request.userid == userid)) 
#     id = session.scalars(get_request_id).all() #.all() #.one() #.first()
#     session.commit()
#     return {"statuts": statuts, "id": id, "userid": userid}

# correction version communication de rimnatt fait un premier post vers l'API (simplifié)

@app.post("/api/v1.0/queue/")
async def createServiceRequest(userid: int, service: str, input: str, statuts: str, step: int):
    request = Request(userid = userid, service = service, input = input, statuts = statuts, step = step)
    session.add(request)
    session.commit()
    return request
    # return {"statuts": statuts, "id": id, "userid": userid}

# # communication de "mnt-diff" qui retourne des infos vers l'API
# @app.post("/api/v1.0/queue/mnt-diff")
# async def createServiceOutput(producer: str, types: str, path: str, size: int): #, reqId: int
#     outputs = Outputs(producer = producer, types = types, path = path, size = size) # , reqId = reqId
#     session.add(outputs)
#     session.commit()
#     return outputs

#--------tentative table assos-------

# communication de "mnt-diff" qui retourne des infos vers l'API
@app.post("/api/v1.0/queue/mnt-diff")
async def createServiceOutputReqoutput(producer: str, types: str, path: str, size: int, reqestId: int): #, reqId: int
    outputs = Outputs(producer = producer, types = types, path = path, size = size, reqestId = [ReqOuputs(reqid = reqestId)]) # , reqId = reqId
    session.add(outputs)
    session.commit()
    return outputs

@app.post("/createidleft/") 
async def create_id_left(): 
    add_id = Parent(id = "1", extra_data = "118")
    session.add(add_id)
    session.commit()  
    return {"entrée d'un id left"}

@app.post("/createidright/") 
async def create_id_right(): 
    add_id = Child(id = "1", extra_data = "118")
    session.add(add_id)
    session.commit()  
    return {"entrée d'un id right"}


##########################
# toute les commande put #
##########################

# update by id, name, fullname
@app.put("/updatePut/{id}/{name}/{fullname}")
async def updatePut(id: int, name: str, fullname: str):
    stmt = (update(Usr).values(name = name, fullname= fullname).where(Usr.id == id))
    session.execute(stmt)
    session.commit()
    return {"Update": id,"name": name,"fullname": fullname}

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
@app.delete("/deleteDel/{id}")
async def deleteDel(id: int):
    add_user = session.query(Usr).get(id)
    session.delete(add_user)
    session.commit()
    return {"delete": id}

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