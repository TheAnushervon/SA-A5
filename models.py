from __future__ import annotations

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)

    messages: Mapped[list[Message]] = relationship("Message", back_populates="user")
    likes: Mapped[list[Like]] = relationship("Like", back_populates="user")
    auth_sessions: Mapped[list[AuthSession]] = relationship("AuthSession", back_populates="user")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False) 
    text = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False)

    user: Mapped[list[Message]] = relationship("User", back_populates="messages")
    likes: Mapped[list[Like]] = relationship("Like", back_populates="message")


class Like(Base):
    __tablename__ = "likes"
    message_id = Column(Integer, ForeignKey("messages.id"), primary_key=True, nullable=False)
    username = Column(String, ForeignKey("users.username"), primary_key=True, nullable=False)

    message: Mapped[Message] = relationship("Message", back_populates="likes")
    user: Mapped[User] = relationship("User", back_populates="likes")


class AuthSession(Base):
    __tablename__ = "auth_sessions"
    token = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    given_at = Column(DateTime, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="auth_sessions")
