from Backend.account_service import generate_account_number
from unittest.mock import patch


@patch("Backend.account_service.sqlitedb")
def test_generate_account_number_length(mock_db):
    mock_db.account_number_exists.return_value = False
    account_number = generate_account_number()
    assert len(account_number) == 7
    assert account_number.isdigit()


@patch("Backend.account_service.sqlitedb")
def test_generate_account_number_checks_database(mock_db):
    mock_db.account_number_exists.return_value = False
    account_number = generate_account_number()
    mock_db.account_number_exists.assert_called_once_with(account_number)


@patch("Backend.account_service.random.randint")
@patch("Backend.account_service.sqlitedb")
def test_generate_account_number_duplicate(
    mock_db,
    mock_randint,
):
    mock_randint.side_effect = [
        1234567,
        7654321,
    ]
    mock_db.account_number_exists.side_effect = [
        True,
        False,
    ]
    account_number = generate_account_number()
    assert account_number == "7654321"
    assert mock_db.account_number_exists.call_count == 2
