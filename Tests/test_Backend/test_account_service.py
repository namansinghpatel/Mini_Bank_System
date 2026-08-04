from Backend.account_service import (
    change_password,
    delete_account,
    generate_account_number,
    transfer_money,
    withdraw_money,
    hash_password,
)
from unittest.mock import patch
from Backend.account_service import get_account_balance, deposit_money
from Backend.account_service import get_transaction_history


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


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_success(mock_db):
    mock_db.get_balance.side_effect = [1000, 500]
    mock_db.transfer_money.return_value = True
    success, message = transfer_money("1001", "1002", "300")
    assert success is True
    assert message == "₹300.00 transferred successfully."
    assert mock_db.get_balance.call_count == 2
    mock_db.transfer_money.assert_called_once_with("1001", "1002", 300.0)


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_invalid_amount(mock_db):
    success, message = transfer_money("1001", "1002", "abc")
    assert success is False
    assert message == "Please enter a valid amount."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_empty_amount(mock_db):
    success, message = transfer_money("1001", "1002", "")
    assert success is False
    assert message == "Please enter a valid amount."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_zero_amount(mock_db):
    success, message = transfer_money("1001", "1002", "0")
    assert success is False
    assert message == "Amount must be greater than zero."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_negative_amount(mock_db):
    success, message = transfer_money("1001", "1002", "-500")
    assert success is False
    assert message == "Amount must be greater than zero."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_sender_not_found(mock_db):
    mock_db.get_balance.return_value = None
    success, message = transfer_money("9999", "1002", "300")
    assert success is False
    assert message == "Sender account not found."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_receiver_not_found(mock_db):
    mock_db.get_balance.side_effect = [1000, None]
    success, message = transfer_money("1001", "9999", "300")
    assert success is False
    assert message == "Receiver account not found."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_same_account(mock_db):
    mock_db.get_balance.side_effect = [1000, 1000]
    success, message = transfer_money("1001", "1001", "300")
    assert success is False
    assert message == "Cannot transfer to the same account."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_insufficient_balance(mock_db):
    mock_db.get_balance.side_effect = [200, 500]

    success, message = transfer_money("1001", "1002", "300")
    assert success is False
    assert message == "Insufficient balance."
    mock_db.transfer_money.assert_not_called()


@patch("Backend.account_service.sqlitedb")
def test_transfer_money_database_failure(mock_db):
    mock_db.get_balance.side_effect = [1000, 500]
    mock_db.transfer_money.return_value = False
    success, message = transfer_money("1001", "1002", "300")
    assert success is False
    assert message == "Transfer failed."
    mock_db.transfer_money.assert_called_once_with("1001", "1002", 300.0)


@patch("Backend.account_service.sqlitedb")
def test_get_transaction_history_success(mock_db):
    mock_db.get_transactions.return_value = [
        ("Deposit", 500.0, 1500.0, "2026-07-27 10:00:00")
    ]
    success, history = get_transaction_history("1001")
    assert success is True
    assert len(history) == 1
    mock_db.get_transactions.assert_called_once_with("1001")


@patch("Backend.account_service.sqlitedb")
def test_get_transaction_history_empty(mock_db):
    mock_db.get_transactions.return_value = []
    success, history = get_transaction_history("1001")
    assert success is True
    assert history == []
    mock_db.get_transactions.assert_called_once_with("1001")


@patch("Backend.account_service.sqlitedb")
def test_get_transaction_history_multiple_records(mock_db):
    mock_db.get_transactions.return_value = [
        ("Withdraw", 200.0, 800.0, "2026-07-27 10:10:00"),
        ("Deposit", 500.0, 1000.0, "2026-07-27 09:30:00"),
    ]
    success, history = get_transaction_history("1001")
    assert success is True
    assert len(history) == 2
    assert history[0][0] == "Withdraw"
    assert history[1][0] == "Deposit"


@patch("Backend.account_service.sqlitedb")
def test_get_transaction_history_transaction_fields(mock_db):
    mock_db.get_transactions.return_value = [
        ("Deposit", 500.0, 1500.0, "2026-07-27 10:00:00")
    ]
    success, history = get_transaction_history("1001")
    assert success is True
    assert len(history[0]) == 4


@patch("Backend.account_service.sqlitedb")
def test_get_transaction_history_database_called(mock_db):
    mock_db.get_transactions.return_value = []
    get_transaction_history("1001")
    mock_db.get_transactions.assert_called_once_with("1001")


@patch("Backend.account_service.sqlitedb")
def test_change_password_success(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("OldPassword123")
    mock_db.update_password.return_value = True
    success, message = change_password("1001", "OldPassword123", "NewPassword123", "NewPassword123")
    assert success is True
    assert message == "Password changed successfully."
    mock_db.update_password.assert_called_once()


@patch("Backend.account_service.sqlitedb")
def test_change_password_wrong_current_password(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("OldPassword123")
    success, message = change_password("1001", "WrongPassword", "NewPassword123", "NewPassword123")
    assert success is False
    assert message == "Current password is incorrect."


@patch("Backend.account_service.sqlitedb")
def test_change_password_passwords_not_match(mock_db):
    success, message = change_password("1001", "OldPassword123", "NewPassword123", "DifferentPassword")
    assert success is False
    assert message == "New passwords do not match."


@patch("Backend.account_service.sqlitedb")
def test_change_password_database_failure(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("OldPassword123")
    mock_db.update_password.return_value = False
    success, message = change_password("1001", "OldPassword123", "NewPassword123", "NewPassword123")
    assert success is False
    assert message == "Password update failed."


@patch("Backend.account_service.sqlitedb")
def test_change_password_empty_current_password(mock_db):
    success, message = change_password("1001", "", "NewPassword123", "NewPassword123")
    assert success is False
    assert message == "Please enter your current password."


@patch("Backend.account_service.sqlitedb")
def test_change_password_empty_new_password(mock_db):
    success, message = change_password(
        "1001",
        "OldPassword123",
        "",
        "")
    assert success is False
    assert message == "Please enter a new password."


@patch("Backend.account_service.sqlitedb")
def test_change_password_empty_confirm_password(mock_db):
    success, message = change_password("1001", "OldPassword123", "NewPassword123", "")
    assert success is False
    assert message == "Please confirm your new password."


@patch("Backend.account_service.sqlitedb")
def test_change_password_short_password(mock_db):
    success, message = change_password("1001", "OldPassword123", "abc", "abc")
    assert success is False
    assert message == "Password must be at least 8 characters long."


@patch("Backend.account_service.sqlitedb")
def test_change_password_account_not_found(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = None
    success, message = change_password("1001", "OldPassword123", "NewPassword123", "NewPassword123")
    assert success is False
    assert message == "Account not found."


@patch("Backend.account_service.sqlitedb")
def test_change_password_same_password(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("Password123")
    success, message = change_password("1001", "Password123", "Password123", "Password123")
    assert success is False
    assert message == "New password must be different from the current password."


@patch("Backend.account_service.sqlitedb")
def test_delete_account_empty_password(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("Password123")
    success, message = delete_account("1001", "")
    assert success is False
    assert message == "Password cannot be empty."


@patch("Backend.account_service.sqlitedb")
def test_delete_account_account_not_found(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = None
    success, message = delete_account("1001", "Password123")
    assert success is False
    assert message == "Account not found."


@patch("Backend.account_service.sqlitedb")
def test_delete_account_invalid_password(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("CorrectPassword")
    success, message = delete_account("1001", "WrongPassword")
    assert success is False
    assert message == "Invalid password."


@patch("Backend.account_service.sqlitedb")
def test_delete_account_database_failure(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("Password123")
    mock_db.delete_account.return_value = False
    success, message = delete_account("1001", "Password123")
    assert success is False
    assert message == "Account deletion failed."


@patch("Backend.account_service.sqlitedb")
def test_delete_account_success(mock_db):
    mock_db.get_user_password_hash_by_account.return_value = hash_password("Password123")
    mock_db.delete_account.return_value = True
    success, message = delete_account("1001", "Password123")
    assert success is True
    assert message == "Account deleted successfully."
    mock_db.delete_account.assert_called_once_with("1001")
