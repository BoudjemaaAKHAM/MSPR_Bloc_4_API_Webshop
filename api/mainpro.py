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

#-----------------table projet----------------------

class Outputs(Base):
    __tablename__ = "outputs"
    date = Column(DateTime, default=datetime.datetime.utcnow)
    id = Column(Integer, primary_key=True)
    producer = Column(String(30))
    types = Column(Enum('txt', 'laz', 'potree'))
    path = Column(String(200))
    size = Column(Integer)
    # requestId = relationship("ReqOutputs", back_populates="output", cascade="all, delete-orphan")
    def __repr__(self):
        return f"Outputs(date={self.date!r}, id={self.id!r}, producer={self.producer!r}, types={self.types!r}, path={self.path!r}, size={self.size!r}, requestId={self.requestId!r})"


class ReqOutputs(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
    __tablename__ = "reqoutputs"
    id = Column(Integer, primary_key=True)
    reqid = Column(Integer, ForeignKey("request.userid"), nullable=False) #, ForeignKey("request.id"), nullable=False , ForeignKey("request.userid")
    outid = Column(Integer, ForeignKey("outputs.id"), nullable=False) #, ForeignKey("outputs.id"), nullable=False
    # outid = Column(Integer, nullable=False)
    # output = relationship("Outputs", back_populates="requestId")
    def __repr__(self):
        return f"Address(id={self.id!r}, reqid={self.reqid!r}, outid={self.outid!r})"

class Request(Base): #TAF a rentrée dans la table : date, id, user-id, service, input, statut, step, output en liaison avec output.id
    __tablename__ = "request"
    id = Column(Integer) #, primary_key=True, autoincrement=True, nullable=False
    date = Column(DateTime, default=datetime.datetime.utcnow)
    userid = Column(Integer, primary_key=True) # , primary_key=True
    service = Column(String(30))
    input = Column(String(500))
    statuts = Column(Enum('Succes', 'In progress', 'Error'))
    step = Column(Integer)
    # output = relationship("Output", back_populates="request")
    # output = relationship("Output", back_populates="request", cascade="all, delete-orphan")
    def __repr__(self):
        return f"Request(date=id={self.id!r}, {self.date!r}, userid={self.userid!r}, service={self.service!r}, input={self.input!r}, statuts={self.statuts!r}, step={self.step!r},)"

#-----------tentative de table intermediaire-------------
# class Association(Base):
#     __tablename__ = "association_table"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     left_id: Mapped[int] = mapped_column(Integer, ForeignKey("left_table.id"), primary_key=True)
#     right_id: Mapped[int] = mapped_column(Integer, ForeignKey("right_table.id"), primary_key=True)
#     # extra_data: Mapped[Optional[str]]
#     # extra_data: Mapped[Optional[int]]
#     child: Mapped["Child"] = relationship()


# class Parent(Base):
#     __tablename__ = "left_table"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     children: Mapped[List["Association"]] = relationship()


# class Child(Base):
#     __tablename__ = "right_table"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
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

#----------------------------------------------------------------------------------------------
# -version pour l'API Ocirn Communication de Mnt-diff qui questionne l'API pour ces informations

#---------------------------------------------------------------------------------
# Mnt-diff lit dans la base de données request si il y a des information pour lui
#---------------------------------------------------------------------------------
@app.get("/api/v1.0/queue/{service}") # {id} besoin de savoir quel micro service demande
async def readStepRequest(service):
    get_request_step_to_do = select(Request).where(Request.service == service).where(Request.step == 0).order_by(asc(Request.date)) # asc desc
    print(get_request_step_to_do)
    reader = session.scalars(get_request_step_to_do).all()
    return reader


###########################
# toute les commande post #
###########################

#----------------------------------------------------------------------------------
# rimnat envoie une demande a executer sous forme de données dans la table reqest
#----------------------------------------------------------------------------------
@app.post("/api/v1.0/queue/")
async def createServiceRequest(userid: int, service: str, input: str, statuts: str, step: int):
    request = Request(userid = userid, service = service, input = input, statuts = statuts, step = step)
    session.add(request)
    session.commit()
    return request
    # return {"statuts": statuts, "id": id, "userid": userid}

# communication de "mnt-diff" qui retourne des infos vers l'API
#----------------------------------------------------------------------------------
# lorsque mntdiff a effectuer ses action il enregistre ses resultats dans Outputs
#----------------------------------------------------------------------------------
@app.post("/api/v1.0/queue/mnt-diff") 
async def createServiceOutput(producer: str, types: str, path: str, size: int, requestId: int): #, requestId: int , reqId: int
    outputs = Outputs(producer = producer, types = types, path = path, size = size) # , requestId = [ReqOutputs(reqid = requestId)]
    session.add(outputs)
    session.commit()
    return outputs, requestId

# TAF
#----------------------------------------------------------------------------------
# lorsque mntdiff a effectuer ses action qu'il a enregistre ses resultats dans Outputs
# il vas mettre l'id outputs et l'userid de request dans la table reqoutput commandé par mntdiff
#----------------------------------------------------------------------------------
# communication de "mnt-diff" qui retourne des infos vers l'API
@app.post("/api/v1.0/queue/mnt") #penser a remetre mnt-diff
async def createServiceReqoutput(outid: int, requesteId: int): #, reqId: int
    reqOutputs = ReqOutputs(reqid = requesteId, outid = outid) #, outid = Outputs.id
    session.add(reqOutputs)
    session.commit()
    return reqOutputs


##########################
# toute les commande put #
##########################
@app.put("/api/v1.0/queue/mnt-diff/{requestId}/{step}")
async def updateStepRequest(requestId: int, step: int):
    StepRequest = (update(Request).values(step = step).where(Request.userid == requestId))
    session.execute(StepRequest)
    session.commit()
    return StepRequest

#############################
# toute les commande delete #
#############################



##########################
# pour lancer le serveur #
##########################
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)