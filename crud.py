from datetime import datetime, timedelta
from typing import Literal
from sqlalchemy.orm import Session
from models import User, AuthSession, Message, Like


def current_time():
    return datetime.now()


def expiration_time(expires_delta: timedelta = None):
    return current_time() + (timedelta(minutes=30) if expires_delta is None else expires_delta)


# CRUD operations for User
def create_user(db: Session, username: str):
    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# CRUD operations for AuthSession


def create_auth_session(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User with username {username} does not exist.")

    auth_session = AuthSession(
        username=user.username,
        token=f"token-{current_time().timestamp()}",
        given_at=current_time(),
        expire_at=expiration_time(),
    )
    db.add(auth_session)
    db.commit()
    db.refresh(auth_session)
    return auth_session


def ping_auth_session(db: Session, token: str):
    auth_session = db.query(AuthSession).filter(
        AuthSession.token == token).first()
    if auth_session and auth_session.expire_at > current_time():
        auth_session.expire_at = expiration_time()
        db.commit()
        return auth_session
    return None


def check_auth_session(db: Session, token: str, ping=True):
    auth_session = db.query(AuthSession).filter(
        AuthSession.token == token).first()
    if auth_session and auth_session.expire_at > current_time():
        if ping:
            auth_session.expire_at = expiration_time()
        db.commit()
        return True
    return False


def deactivate_session(db: Session, token: str):
    session = db.query(AuthSession).filter(AuthSession.token == token).first()
    if session:
        session.expire_at = current_time()
        db.commit()
        return session
    return None


def get_active_sessions(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return db.query(AuthSession).filter(
        AuthSession.username == user.username,
        AuthSession.expire_at > current_time()
    ).all()


def get_auth_session(db: Session, token: str):
    auth_session = db.query(AuthSession).filter(
        AuthSession.token == token).first()
    if not auth_session:
        raise ValueError(f"AuthSession with token {token} does not exist.")
    return auth_session

# CRUD operations for Message


def create_message(db: Session, username: str, text: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User with username {username} does not exist.")

    message = Message(
        username=user.username,
        text=text,
        time=current_time()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_by_user(db: Session, username: str, sort_order: Literal['ask', 'desc'] = "asc"):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User with username {username} does not exist.")

    query = db.query(Message).filter(Message.username == user.username)

    if sort_order == "desc":
        query = query.order_by(Message.time.desc())
    else:
        query = query.order_by(Message.time.asc())

    return query.all()


def get_last_n_messages(db: Session, n: int, sort_order: Literal['asc', 'desc'] = "desc"):
    """
    Retrieve the last n messages from the database, sorted by time.

    :param n: The number of messages to retrieve
    :param sort_order: 'asc' for ascending or 'desc' for descending
    :return: List of Message objects
    """
    query = db.query(Message)

    if sort_order == "desc":
        query = query.order_by(Message.time.desc())
    else:
        query = query.order_by(Message.time.asc())

    return query.limit(n).all()


def delete_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False

# CRUD operations for Like


def like_message(db: Session, username: str, message_id: int):
    user = db.query(User).filter(User.username == username).first()
    message = db.query(Message).filter(Message.id == message_id).first()

    if not user or not message:
        raise ValueError("Invalid user or message.")

    try:
        like = Like(username=user.username, message_id=message.id)
    except IndentationError:
        raise ValueError(
            f"Message {message_id} already liked by {username}") from None

    db.add(like)
    db.commit()
    return like


def unlike_message(db: Session, username: str, message_id: int):
    user = db.query(User).filter(User.username == username).first()
    like = db.query(Like).filter(
        Like.username == user.username,
        Like.message_id == message_id
    ).first()

    if like:
        db.delete(like)
        db.commit()
        return True
    return False
