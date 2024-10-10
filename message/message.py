from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

import crud
import models
import database
from sqlalchemy.orm import Session

app = FastAPI()

def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=database.engine)    
    yield  # The app runs between yield points
    print("Shutting down...")

class Message(BaseModel):
    username: str
    message: str

@app.post("/message/{message_id}/like")
def like_message(message_id: int, token: str, db: Session = Depends(database.get_db)):
    if not crud.check_auth_session(token, db):
        raise HTTPException(status_code=400, detail='Unauthorized access')
    
    auth_session = crud.get_auth_session(token, db)

    username = auth_session.username

    try:
        like = crud.like_message(db, username, message_id)
        return {"status": "success", "like": like}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/message/{message_id}/unlike")
def unlike_message(message_id: int, token: str, db: Session = Depends(database.get_db)):
    if not crud.check_auth_session(token, db):
        raise HTTPException(status_code=400, detail='Unauthorized access')
    
    auth_session = crud.get_auth_session(token, db)

    username = auth_session.username

    if crud.unlike_message(db, username, message_id):
        return {"status": "success", "like": ''}
    else:
        raise HTTPException(status_code=400, detail=f"Message {message_id} was not liked by {username}")


@app.post("/message")
def create_message(message: Message, token: str, db: Session = Depends(database.get_db)):
    if not crud.check_auth_session(token, db):
        raise HTTPException(status_code=400, detail='Unauthorized access')
    

    try:
        crud.create_message(db, message.username, message.message)
        return {"message": f"<{message.username}> has added <{message.message}>"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
