from Backend.account_service import generate_account_number, withdraw_money
from unittest.mock import patch
from Backend.account_service import get_account_balance, deposit_money


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
def test_generate_account_number_duplicate(mock_db, mock_randint):
    mock_randint.side_effect = [1234567, 7654321]
    mock_db.account_number_exists.side_effect = [True, False]
    account_number = generate_account_number()
    assert account_number == "7654321"
    assert mock_db.account_number_exists.call_count == 2


# ==========================================================
# GET ACCOUNT BALANCE TESTS
# ==========================================================


@patch("Backend.account_service.sqlitedb")
def test_get_account_balance_success(mock_db):
    mock_db.get_balance.return_value = 500.0
    success, result = get_account_balance("1234567")
    assert success
    assert result == 500.0
    mock_db.get_balance.assert_called_once_with("1234567")


@patch("Backend.account_service.sqlitedb")
def test_get_account_balance_account_not_found(mock_db):
    mock_db.get_balance.return_value = None
    success, result = get_account_balance("9999999")
    assert not success
    assert result == "Account not found"
    mock_db.get_balance.assert_called_once_with("9999999")


# ==========================================================
# DEPOSIT MONEY TESTS
# ==========================================================


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_success(
    mock_db,
):
    mock_db.deposit_money.return_value = True
    success, message = deposit_money("1234567", "500")
    assert success
    assert message == ("₹500.00 deposited successfully.")
    mock_db.deposit_money.assert_called_once_with("1234567", 500.0)


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_invalid_amount(mock_db):
    success, message = deposit_money("1234567", "hello")
    assert not success
    assert message == ("Please enter a valid amount.")
    mock_db.deposit_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_empty_amount(mock_db):
    success, message = deposit_money("1234567", "")
    assert not success
    assert message == ("Please enter a valid amount.")
    mock_db.deposit_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_zero_amount(mock_db):
    success, message = deposit_money("1234567", "0")
    assert not success
    assert message == ("Amount must be greater than zero.")
    mock_db.deposit_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_negative_amount(
    mock_db,
):
    success, message = deposit_money("1234567", "-500")
    assert not success
    assert message == ("Amount must be greater than zero.")
    mock_db.deposit_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_deposit_money_account_not_found(mock_db):
    mock_db.deposit_money.return_value = False
    success, message = deposit_money("9999999", "500")
    assert not success
    assert message == "Account not found."
    mock_db.deposit_money.assert_called_once_with("9999999", 500.0)


@patch("Backend.account_service.sqlitedb")
def test_withdraw_money_success(mock_db):
    mock_db.get_balance.return_value = 1000
    mock_db.withdraw_money.return_value = True
    success, message = withdraw_money("1234567", "300")
    assert success is True
    assert message == "₹300.00 withdrawn successfully."
    mock_db.withdraw_money.assert_called_once_with("1234567", 300.0)


@patch("Backend.account_service.sqlitedb")
def test_withdraw_invalid_amount(mock_db):
    success, message = withdraw_money("1234567", "abc")
    assert success is False
    assert message == "Please enter a valid amount."
    mock_db.get_balance.assert_not_called()
    mock_db.withdraw_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_withdraw_negative_amount(mock_db):
    success, message = withdraw_money("1234567", "-500")
    assert success is False
    assert message == "Amount must be greater than zero."
    mock_db.get_balance.assert_not_called()
    mock_db.withdraw_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_withdraw_zero_amount(mock_db):
    success, message = withdraw_money("1234567", "0")
    assert success is False
    assert message == "Amount must be greater than zero."
    mock_db.get_balance.assert_not_called()
    mock_db.withdraw_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_withdraw_account_not_found(mock_db):
    mock_db.get_balance.return_value = None
    success, message = withdraw_money("1234567", "500")
    assert success is False
    assert message == "Account not found."
    mock_db.withdraw_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_withdraw_insufficient_balance(mock_db):
    mock_db.get_balance.return_value = 400
    success, message = withdraw_money("1234567", "500")
    assert success is False
    assert message == "Insufficient balance."
    mock_db.withdraw_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_withdraw_database_failure(mock_db):
    mock_db.get_balance.return_value = 1000
    mock_db.withdraw_money.return_value = False
    success, message = withdraw_money("1234567", "200")
    assert success is False
    assert message == "Withdrawal failed."
