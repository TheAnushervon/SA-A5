from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
app = FastAPI()


SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    message = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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