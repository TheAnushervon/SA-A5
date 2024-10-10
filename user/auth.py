from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import get_db
import database
import models  # assuming you have a function that provides a database session

app = FastAPI()

def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=database.engine)    
    yield  # The app runs between yield points
    print("Shutting down...")


@app.post("/auth/register")
def register_user(username: str, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(crud.User).filter(crud.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    # Create a new user
    try:
        new_user = crud.create_user(db, username)
        
        # Auto-login by creating an auth session and issuing a token
        auth_session = crud.create_auth_session(db, new_user.username)
        return {"message": "User registered successfully", "token": auth_session.token, "expires_at": auth_session.expire_at}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during registration")
    


@app.post("/auth/login")
def login_user(username: str, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(crud.User).filter(crud.User.username == username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Issue a new token by creating an auth session
    try:
        auth_session = crud.create_auth_session(db, username)
        return {"message": "Login successful", "token": auth_session.token, "expires_at": auth_session.expire_at}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during login")



@app.post("/auth/logout")
def logout_user(token: str, db: Session = Depends(get_db)):
    # Try to deactivate the token
    try:
        deactivated_session = crud.deactivate_session(db, token)
        if not deactivated_session:
            raise HTTPException(status_code=400, detail="Invalid token")
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during logout")