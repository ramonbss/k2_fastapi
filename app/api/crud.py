from contextlib import contextmanager
from sqlalchemy.orm import Session
from .database import Admin, BaseUser, Purchase, Report, User, DatabaseSessionLocal


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


def get_user_by_token(token: str, instance: type[BaseUser]):
    """Retrieve a user by their token."""
    with get_db_session() as db:
        return db.query(instance).filter(instance.token == token).first()


def get_user_by_id(id: int):
    """Retrieve a user by their email."""
    with get_db_session() as db:
        return db.query(User).filter(User.id == id).first()


def get_admin_by_id(id: int):
    """Retrieve a user by their email."""
    with get_db_session() as db:
        return db.query(Admin).filter(Admin.id == id).first()


def get_user_by_username(username: str, instance: type[BaseUser]):
    """Retrieve a user by their username."""
    with get_db_session() as db:
        return db.query(instance).filter(instance.username == username).first()


def get_user_by_email(email: str):
    """Retrieve a user by their email."""
    with get_db_session() as db:
        return db.query(User).filter(User.email == email).first()


def reset_access_token(token: str, instance: type[BaseUser]):
    with get_db_session() as db:
        user = get_user_by_token(token, instance)
        user.token = ""
        db.add(user)
        db.commit()
        db.refresh(user)


def create_or_update_user(username: str, role: str, token: str):
    with get_db_session() as db:
        """Save or update User/Admin data."""
        instance = User if role == "user" else Admin
        user = get_user_by_username(username, instance)
        if user:
            # Update existing user
            user.role = role
            user.token = token
        else:
            # Create new user
            user = instance(username=username, role=role, token=token)
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
    user = get_user_by_username(username, "user")
    if user:
        return get_user_purchases_from_db(user.id)


def get_user_purchases_by_email(db: Session, user_email: str):
    """Retrieve a user's purchases by their email."""
    user = get_user_by_email(db, user_email)
    if user:
        return get_user_purchases_from_db(db, user.id)
    return


def create_purchases(token: str, purchases_data: dict):
    """Save or update user authentication data."""
    with get_db_session() as db:
        user = get_user_by_token(token, User)
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


def get_admin_reports_from_db(user_id: int):
    """Retrieve a admin's reports."""
    with get_db_session() as db:
        return db.query(Report).filter(Report.user_id == user_id).all()


def create_reports(admin_token: str, reports_data: dict):
    """Save or update user authentication data."""
    with get_db_session() as db:
        user = get_user_by_token(admin_token, Admin)
        reports = reports_data["reports"]

        for r in reports:
            r["user_id"] = user.id
            report = Report(**r)
            db.add(report)

        name = reports_data["name"]
        email = reports_data["email"]

        user.name = name
        user.email = email

        db.add(user)

        db.commit()
        db.refresh(user)
        return user
