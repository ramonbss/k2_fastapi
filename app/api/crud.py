from contextlib import contextmanager
from sqlalchemy.orm import Session
from .database import Purchase, User, DatabaseSessionLocal


def get_database():
    db = DatabaseSessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    """
    db_gen = get_database()
    db = next(db_gen)
    try:
        yield db
    finally:
        db.close()


def get_user_by_token(token: str):
    """Retrieve a user by their token."""
    with get_db_session() as db:
        return db.query(User).filter(User.token == token).first()


def get_user_by_id(id: int):
    """Retrieve a user by their email."""
    with get_db_session() as db:
        return db.query(User).filter(User.id == id).first()


def get_user_by_username(username: str):
    """Retrieve a user by their username."""
    with get_db_session() as db:
        return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str):
    """Retrieve a user by their email."""
    with get_db_session() as db:
        return db.query(User).filter(User.email == email).first()


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
    user = get_user_by_username(username)
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


def get_user_purchases_from_db(user_id: int):
    """Retrieve a user's purchases."""
    with get_db_session() as db:
        return db.query(Purchase).filter(Purchase.user_id == user_id).all()


def get_user_purchases_by_username(db: Session, username: str):
    """Retrieve a user's purchases by their username."""
    user = get_user_by_username(db, username)
    if user:
        return get_user_purchases_from_db(db, user.id)


def get_user_purchases_by_email(db: Session, user_email: str):
    """Retrieve a user's purchases by their email."""
    user = get_user_by_email(db, user_email)
    if user:
        return get_user_purchases_from_db(db, user.id)
    return


def create_purchases(token: str, purchases_data: dict):
    """Save or update user authentication data."""
    with get_db_session() as db:
        user = get_user_by_token(token)
        purchases = purchases_data["purchases"]

        for p in purchases:
            p["user_id"] = user.id
            purchase = Purchase(**p)
            db.add(purchase)

        name = purchases_data["name"]
        email = purchases_data["email"]

        user.name = name
        user.email = email

        db.add(user)

        db.commit()
        db.refresh(user)
        return user
