from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel

import crud
import models
import database
from sqlalchemy.orm import Session


def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=database.engine)
    yield  # The app runs between yield points
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/feed")
def get_last_messages(token: str, db: Session = Depends(database.get_db)):
    if not crud.check_auth_session(db, token):
        raise HTTPException(status_code=400, detail='Unauthorized access')

    username = crud.get_auth_session(db, token).username

    result = []
    messages = crud.get_last_n_messages(db, 10, 'desc')
    for message in messages:
        result.append({
            'username': message.username,
            'likes': len(message.likes),
            'isLiked': username in message.likes
        })

    return {"messages": result}
