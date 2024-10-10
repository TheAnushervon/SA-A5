from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import MessageModel
from database import get_db
app = FastAPI()

class Message(BaseModel):
    username: str
    message: str


@app.post("/message")
def add_message(message: Message, db: Session = Depends(get_db)):
    db_message = MessageModel(username=message.username, message=message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"message": f"<{message.username}> has added <{message.message}>"}

@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(MessageModel).all()
    return {"messages": messages}

@app.get("/feed")
def get_feed (db: Session = Depends(get_db)): 
    result = db.query(MessageModel).all()
    return {"result": result}


    