import datetime

from Backend.auth_service import create_user, login_user
from unittest.mock import patch
from Backend.security import hash_password


@patch("Backend.auth_service.sqlitedb")
def test_create_new_user(mock_db):
    mock_db.user_exists.return_value = False
    success, message = create_user("new_user_1", "password123", "password123")
    assert success
    assert message == "Account Created Successfully"
    mock_db.user_exists.assert_called_once_with("new_user_1")
    mock_db.create_user.assert_called_once()


@patch("Backend.auth_service.sqlitedb")
def test_create_duplicate_user(mock_db):
    mock_db.user_exists.return_value = True
    success, message = create_user("duplicate_user", "password123", "password123")
    assert not success
    assert message == "Username already exists"
    mock_db.user_exists.assert_called_once_with("duplicate_user")
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_password_mismatch(mock_db):
    success, message = create_user("userx", "password123", "password321")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_short_username(mock_db):
    success, message = create_user("ab", "password123", "password123")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_short_password(mock_db):
    success, message = create_user("prashant", "123", "123")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_success(mock_db):
    mock_db.user_exists.return_value = False
    success, message = create_user("new_user", "password123", "password123")
    assert success
    assert message == "Account Created Successfully"
    mock_db.user_exists.assert_called_once_with("new_user")
    mock_db.create_user.assert_called_once()
    username, hashed_password = mock_db.create_user.call_args.args
    assert username == "new_user"
    assert hashed_password != "password123"
    assert hashed_password.startswith("$2b$")


@patch("Backend.auth_service.sqlitedb")
def test_create_user_database_failure(mock_db):
    mock_db.user_exists.return_value = False
    mock_db.create_user.side_effect = Exception("Database Down")
    try:
        create_user(
            "new_user",
            "password123",
            "password123",
        )
    except Exception as e:
        assert str(e) == "Database Down"
        return
    pytest.fail("Expected Exception was not raised")


@patch("Backend.auth_service.sqlitedb")
def test_login_success(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    success, message = login_user("login_user", "password123")
    assert success
    assert message == "Login Successful"
    mock_db.reset_login_attempts.assert_called_once_with("login_user")


@patch("Backend.auth_service.sqlitedb")
def test_login_wrong_password(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    mock_db.get_failed_attempts.return_value = 0
    success, message = login_user("login_user2", "wrongpassword")
    assert not success
    mock_db.update_failed_attempts.assert_called_once_with("login_user2", 1)


@patch("Backend.auth_service.sqlitedb")
def test_login_unknown_user(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = None
    success, message = login_user("unknown_user", "password123")
    assert not success
    assert message == "Invalid Username or Password"


@patch("Backend.auth_service.sqlitedb")
def test_login_empty_username(mock_db):
    success, message = login_user("", "password123")
    assert not success
    mock_db.get_locked_until.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_login_empty_password(mock_db):
    success, message = login_user("prashant", "")
    assert not success
    mock_db.get_locked_until.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_login_database_success(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    success, _ = login_user("prashant", "password123")
    assert success


@patch("Backend.auth_service.sqlitedb")
def test_login_database_failure(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.side_effect = Exception("Database Down")
    try:
        login_user("prashant", "password123")
        assert False
    except Exception as e:
        assert str(e) == "Database Down"


@patch("Backend.auth_service.sqlitedb")
def test_login_locked_account(mock_db):
    mock_db.get_locked_until.return_value = "2099-01-01T00:00:00"
    success, message = login_user("prashant", "password123")
    assert not success
    assert "Account locked" in message


@patch("Backend.auth_service.sqlitedb")
def test_login_locks_account_after_third_attempt(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    mock_db.get_failed_attempts.return_value = 2
    success, message = login_user("prashant", "wrongpassword")
    assert not success
    assert (
        message == "Account locked for 1 minute due to multiple failed login attempts."
    )
    mock_db.update_failed_attempts.assert_called_once_with("prashant", 3)
    mock_db.lock_user.assert_called_once()


@patch("Backend.auth_service.sqlitedb")
def test_lock_user_called_after_three_failures(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    mock_db.get_failed_attempts.return_value = 2
    login_user("prashant", "wrongpassword")
    assert mock_db.lock_user.called


@patch("Backend.auth_service.sqlitedb")
def test_lock_user_receives_timestamp(mock_db):
    mock_db.get_locked_until.return_value = None
    mock_db.get_user_password_hash.return_value = hash_password("password123")
    mock_db.get_failed_attempts.return_value = 2
    login_user("prashant", "wrongpassword")
    args = mock_db.lock_user.call_args
    username = args[0][0]
    timestamp = args[0][1]
    assert username == "prashant"
    assert isinstance(timestamp, str)


@patch("Backend.auth_service.generate_account_number")
@patch("Backend.auth_service.sqlitedb")
def test_create_user_generates_account_number(
    mock_db,
    mock_generate_account_number,
):
    mock_db.user_exists.return_value = False
    mock_generate_account_number.return_value = "1234567"
    success, message = create_user(
        "prashant",
        "password123",
        "password123",
    )
    assert success
    mock_generate_account_number.assert_called_once()
    mock_db.create_user.assert_called_once()


@patch("Backend.auth_service.generate_account_number")
@patch("Backend.auth_service.sqlitedb")
def test_create_user_stores_generated_account_number(
    mock_db,
    mock_generate_account_number,
):
    mock_db.user_exists.return_value = False
    mock_generate_account_number.return_value = "7654321"
    success, _ = create_user(
        "prashant",
        "password123",
        "password123",
    )
    args = mock_db.create_user.call_args[0]
    assert args[0] == "7654321"
    assert args[1] == "prashant"
    assert success
