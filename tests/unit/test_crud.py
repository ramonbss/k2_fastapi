import pytest
from unittest.mock import MagicMock, patch
from app.api.crud import (
    create_or_update_user,
    get_user_by_username,
    get_user_purchases_from_db,
    create_purchases,
    get_admin_reports_from_db,
    create_reports,
    get_user_by_token,
    get_user_by_id,
    get_admin_by_id,
)
from app.core.config import ROLE_ADMIN, ROLE_USER


# Mocking thea database session
@pytest.fixture
def mock_db_session2(mocker):
    mock_session = MagicMock()
    mocker.patch("crud.get_db_session", return_value=mock_session)
    return mock_session


@pytest.fixture
def mock_db_session():
    """
    Mock database session fixture.
    """
    with patch("app.api.crud.get_db_session") as mock_session:
        db = MagicMock()
        mock_session.return_value.__enter__.return_value = db
        yield db


def test_get_user_by_token(mock_db_session):
    mock_user = MagicMock()
    mock_user.token = "testtoken"
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_user
    )

    result = get_user_by_token("testtoken", MagicMock())

    assert result == mock_user
    mock_db_session.query.assert_called_once()


def test_get_user_by_id(mock_db_session):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_user
    )

    result = get_user_by_id(1)

    assert result == mock_user
    mock_db_session.query.assert_called_once()


def test_get_admin_by_id(mock_db_session):
    mock_admin = MagicMock()
    mock_admin.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_admin
    )

    result = get_admin_by_id(1)

    assert result == mock_admin
    mock_db_session.query.assert_called_once()


def test_get_user_by_username(mock_db_session):
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_user
    )

    result = get_user_by_username("testuser", MagicMock())

    assert result == mock_user
    mock_db_session.query.assert_called_once()


def test_create_or_update_user(mock_db_session):

    # Simulate no existing user in the database (create case)
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = create_or_update_user("testuser", ROLE_USER, "testtoken")

    # Assertions for created user
    assert result.username == "testuser"
    assert result.role == ROLE_USER
    assert result.token == "testtoken"

    # Verify database calls
    mock_db_session.add.assert_called_once_with(result)
    mock_db_session.commit.assert_called_once()


def test_create_or_update_existing_user(mock_db_session):

    # Simulate an existing user in the database (update case)
    existing_user = MagicMock(username="testuser", role=ROLE_USER, token="oldtoken")
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        existing_user
    )

    create_or_update_user("testuser", ROLE_ADMIN, "newtoken")

    # Assertions for updated user
    assert existing_user.role == ROLE_ADMIN
    assert existing_user.token == "newtoken"

    # Verify database calls
    mock_db_session.commit.assert_called_once()


def test_get_user_purchases_from_db(mock_db_session):

    # Mock purchase data for a user ID
    purchase_1, purchase_2 = MagicMock(), MagicMock()
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        purchase_1,
        purchase_2,
    ]

    result = get_user_purchases_from_db(1)

    # Assertions
    assert result == [purchase_1, purchase_2]
    mock_db_session.query.assert_called_once()
    mock_db_session.query.return_value.filter.assert_called_once()
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()


def test_create_purchases(mock_db_session):

    # Mock user and purchase data
    mock_user = MagicMock()
    mock_user.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_user
    )

    purchases_data = {
        "purchases": [
            {"item": "Laptop", "price": 2500},
            {"item": "Smartphone", "price": 1200},
        ],
        "name": "John Doe",
        "email": "john@example.com",
    }

    result = create_purchases("testtoken", purchases_data)

    # Assertions
    assert result.name == "John Doe"
    assert result.email == "john@example.com"
    assert len(mock_db_session.add.call_args_list) == 3  # 2 purchases + 1 user
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_user)


def test_get_admin_reports_from_db(mock_db_session):

    # Mock report data for an admin ID
    report_1, report_2 = MagicMock(), MagicMock()
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        report_1,
        report_2,
    ]

    result = get_admin_reports_from_db(1)

    # Assertions
    assert result == [report_1, report_2]
    mock_db_session.query.assert_called_once()
    mock_db_session.query.return_value.filter.assert_called_once()
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()


def test_create_reports(mock_db_session):

    # Mock admin and report data
    mock_admin = MagicMock()
    mock_admin.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        mock_admin
    )

    reports_data = {
        "reports": [
            {"title": "Report 1", "status": "Pending"},
            {"title": "Report 2", "status": "Completed"},
        ],
        "name": "Admin User",
        "email": "admin@example.com",
    }

    result = create_reports("admintoken", reports_data)

    # Assertions
    assert result.name == "Admin User"
    assert result.email == "admin@example.com"
    assert len(mock_db_session.add.call_args_list) == 3  # 2 reports + 1 admin
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_admin)
