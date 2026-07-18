from unittest.mock import MagicMock, patch
from GUI.withdraw_page import WithdrawPage


def test_set_account(qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    assert page.account_number == "1234567"
    assert page.account_label.text() == ("🏦 Account Number : 1234567")
    assert page.amount.text() == ""


def test_back_clicked(qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.amount.setText("500")
    page.back_clicked()
    stack.setCurrentIndex.assert_called_once_with(2)
    assert page.amount.text() == ""


@patch("GUI.withdraw_page.withdraw_money")
@patch("GUI.withdraw_page.QMessageBox.information")
def test_withdraw_success(mock_information, mock_withdraw, qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    page.amount.setText("500")
    mock_withdraw.return_value = (True, "₹500.00 withdrawn successfully.")
    page.withdraw_clicked()
    mock_withdraw.assert_called_once_with("1234567", "500")
    mock_information.assert_called_once()
    assert page.amount.text() == ""


@patch("GUI.withdraw_page.withdraw_money")
@patch("GUI.withdraw_page.QMessageBox.warning")
def test_withdraw_failure(mock_warning, mock_withdraw, qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    page.amount.setText("500")
    mock_withdraw.return_value = (False, "Insufficient balance.")
    page.withdraw_clicked()
    mock_withdraw.assert_called_once_with("1234567", "500")
    mock_warning.assert_called_once()
    assert page.amount.text() == "500"


def test_account_label_updated(qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.set_account("7654321")
    assert "7654321" in page.account_label.text()


@patch("GUI.withdraw_page.withdraw_money")
@patch("GUI.withdraw_page.QMessageBox.warning")
def test_empty_amount(mock_warning, mock_withdraw, qtbot):
    stack = MagicMock()
    page = WithdrawPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    page.amount.setText("")
    mock_withdraw.return_value = (False, "Please enter a valid amount.")
    page.withdraw_clicked()
    mock_withdraw.assert_called_once_with("1234567", "")
    mock_warning.assert_called_once()
