from unittest.mock import MagicMock, patch
from GUI.deposit_page import DepositPage


def test_deposit_page_creation(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    assert page is not None


def test_deposit_amount_field_exists(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    assert page.amount is not None


def test_deposit_button_exists(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    assert page.deposit_btn is not None


def test_deposit_back_button_exists(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    assert page.back_btn is not None


def test_set_account(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    assert page.account_number == "1234567"
    assert page.account_label.text() == ("🏦 Account Number : 1234567")


@patch("GUI.deposit_page.QMessageBox.information")
@patch("GUI.deposit_page.deposit_money")
def test_deposit_success(mock_deposit_money, mock_information, qtbot):
    stack = MagicMock()
    mock_deposit_money.return_value = (True, "₹500.00 deposited successfully.")
    page = DepositPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    page.amount.setText("500")
    page.deposit_clicked()
    mock_deposit_money.assert_called_once_with("1234567", "500")
    mock_information.assert_called_once_with(
        page, "Success", "₹500.00 deposited successfully."
    )
    assert page.amount.text() == ""


@patch("GUI.deposit_page.QMessageBox.warning")
@patch("GUI.deposit_page.deposit_money")
def test_deposit_failure(mock_deposit_money, mock_warning, qtbot):
    stack = MagicMock()
    mock_deposit_money.return_value = (False, "Amount must be greater than zero.")
    page = DepositPage(stack)
    qtbot.addWidget(page)
    page.set_account("1234567")
    page.amount.setText("-500")
    page.deposit_clicked()
    mock_deposit_money.assert_called_once_with("1234567", "-500")
    mock_warning.assert_called_once_with(
        page, "Deposit Failed", "Amount must be greater than zero."
    )


def test_deposit_back_clicked(qtbot):
    stack = MagicMock()
    page = DepositPage(stack)
    qtbot.addWidget(page)
    page.amount.setText("500")
    page.back_clicked()
    assert page.amount.text() == ""
    stack.setCurrentIndex.assert_called_once_with(2)
