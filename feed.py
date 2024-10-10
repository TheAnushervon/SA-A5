from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import Message
from database import get_db
from crud import get_last_n_messages
app = FastAPI()

class Message(BaseModel):
    username: str
    message: str

@app.get("/feed")
def get_feed (db: Session = Depends(get_db)): 
    result = get_last_n_messages(Depends(get_db), 10, "desc")
    return {"result": result}


    