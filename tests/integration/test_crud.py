from contextlib import contextmanager
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.crud import (
    create_or_update_user,
    get_admin_reports_from_db,
    get_user_by_token,
    get_user_purchases_from_db,
    create_purchases,
    create_reports,
    reset_access_token,
)
from app.api.database import Base, User, Admin, Purchase, Report

# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Test engine and session
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    """
    Create a new database session for a test.
    """
    # Create all tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def override_get_db_session(monkeypatch):
    """
    Override the get_db_session function to use the test database session.
    This fixture is automatically applied to all tests.
    """

    @contextmanager
    def _get_test_db_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Use monkeypatch to override the original get_db_session function
    monkeypatch.setattr("app.api.crud.get_db_session", _get_test_db_session)


def test_create_or_update_user(test_db):

    # Create a new user
    user = create_or_update_user("testuser", "user", "testtoken")

    # Verify user creation
    assert user.username == "testuser"
    assert user.role == "user"
    assert user.token == "testtoken"

    # Update the same user with a new token and role
    updated_user = create_or_update_user("testuser", "admin", "newtoken")

    # Verify user update
    assert updated_user.username == "testuser"
    assert updated_user.role == "admin"  # Role updated
    assert updated_user.token == "newtoken"  # Token updated

    # Check that only one record exists in the database
    users_in_db = test_db.query(User).all()
    assert len(users_in_db) == 1


def test_get_user_by_token(test_db):

    # Insert a user into the test database
    user = User(username="testuser", role="user", token="testtoken")
    test_db.add(user)
    test_db.commit()

    # Retrieve the user by token
    retrieved_user = get_user_by_token("testtoken", User)

    # Verify retrieval
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"


def test_get_user_purchases_from_db(test_db):

    # Insert a user and purchases into the test database
    user = User(username="testuser", role="user", token="testtoken")
    purchase_1 = Purchase(item="Laptop", price=2500, user_id=1)
    purchase_2 = Purchase(item="Smartphone", price=1200, user_id=1)

    test_db.add(user)
    test_db.add(purchase_1)
    test_db.add(purchase_2)
    test_db.commit()

    # Retrieve purchases for the user
    purchases = get_user_purchases_from_db(1)

    # Verify retrieval
    assert len(purchases) == 2
    assert purchases[0].item == "Laptop"


def test_create_purchases(test_db):

    # Insert a user into the test database
    user = User(username="testuser", role="user", token="testtoken")
    test_db.add(user)
    test_db.commit()

    # Prepare purchase data
    purchases_data = {
        "purchases": [
            {"item": "Laptop", "price": 2500},
            {"item": "Smartphone", "price": 1200},
        ],
        "name": "John Doe",
        "email": "john@example.com",
    }

    # Create purchases for the user
    result = create_purchases("testtoken", purchases_data)

    # Verify that purchases were created and associated with the correct user
    assert result.name == "John Doe"


def test_get_admin_reports_from_db(test_db):

    # Insert an admin and reports into the test database
    admin = Admin(username="adminuser", role="admin", token="admintoken")
    report_1 = Report(title="Report 1", status="Pending", user_id=1)
    report_2 = Report(title="Report 2", status="Completed", user_id=1)

    test_db.add(admin)
    test_db.add(report_1)
    test_db.add(report_2)
    test_db.commit()

    # Retrieve reports for the admin
    reports = get_admin_reports_from_db(1)

    # Verify retrieval
    assert len(reports) == 2
    assert reports[0].title == "Report 1"
    assert reports[1].status == "Completed"


def test_create_reports(test_db):

    # Insert an admin into the test database
    admin = Admin(username="adminuser", role="admin", token="admintoken")
    test_db.add(admin)
    test_db.commit()

    # Prepare report data
    reports_data = {
        "reports": [
            {"title": "Report 1", "status": "Pending"},
            {"title": "Report 2", "status": "Completed"},
        ],
        "name": "Admin User",
        "email": "admin@example.com",
    }

    # Create reports for the admin
    result = create_reports("admintoken", reports_data)

    # Verify that reports were created and associated with the correct admin
    assert result.name == "Admin User"
    assert result.email == "admin@example.com"

    # Verify that two reports were added to the database
    reports_in_db = test_db.query(Report).filter(Report.user_id == admin.id).all()
    assert len(reports_in_db) == 2


def test_reset_access_token(test_db):

    # Insert a user into the test database
    user = User(username="testuser", role="user", token="testtoken")
    test_db.add(user)
    test_db.commit()

    # Reset the user's access token
    reset_access_token("testtoken", User)

    # Verify that the token was reset
    updated_user = test_db.query(User).filter(User.username == "testuser").first()
    assert updated_user.token == ""
