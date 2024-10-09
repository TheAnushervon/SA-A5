from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Message(BaseModel):
    username: str
    message: str
    
@app.post("/message")
def message(message: Message):
    return {"message": f"<{message.username}> has added <{message.message}>"}

# @app.post("/message/add")
# def add_message(item): 
#     return {"message": "Message created", "item": item}