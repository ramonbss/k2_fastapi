from sqlalchemy.orm import Session
from .database import User, DatabaseSessionLocal


def get_user_by_token(db: Session, token: str):
    """Retrieve a user by their token."""
    return db.query(User).filter(User.token == token).first()


def get_user_by_username(db: Session, username: str):
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == username).first()


def reset_access_token(token: str):
    try:
        db = DatabaseSessionLocal()
        user = get_user_by_token(db, token)
        user.token = ""
        db.commit()
        db.refresh(user)
    finally:
        db.close()


def create_or_update_user(db: Session, username: str, role: str, token: str):
    """Save or update user authentication data."""
    user = get_user_by_username(db, username)
    if user:
        # Update existing user
        user.role = role
        user.token = token
    else:
        # Create new user
        user = User(username=username, role=role, token=token)
        db.add(user)
    db.commit()
    db.refresh(user)
    return user
