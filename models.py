from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MessageModel(Base):
    __tablename__ = "db-main"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    message = Column(Text)