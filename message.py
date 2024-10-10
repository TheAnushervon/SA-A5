from fastapi import FastAPI, Depends
from pydantic import BaseModel

import models
import database
from sqlalchemy.orm import Session

app = FastAPI()

class Message(BaseModel):
    username: str
    message: str

def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=database.engine)    
    yield  # The app runs between yield points
    print("Shutting down...")



@app.post("/message")
def add_message(message: Message, db: Session = Depends(database.get_db)):
    db_message = Message(username=message.username, message=message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"message": f"<{message.username}> has added <{message.message}>"}

@app.get("/messages")
def get_messages(db: Session = Depends(database.get_db)):
    messages = db.query(Message).all()
    return {"messages": messages}

@app.get("/feed")
def get_feed (db: Session = Depends(database.get_db)): 
    ...

    