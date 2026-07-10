from unittest.mock import MagicMock, patch
from GUI.balance_page import BalancePage


def test_balance_page_creation(qtbot):
    stack = MagicMock()
    page = BalancePage(stack)
    qtbot.addWidget(page)
    assert page is not None


def test_balance_label_exists(qtbot):
    stack = MagicMock()
    page = BalancePage(stack)
    qtbot.addWidget(page)
    assert page.balance_label is not None


@patch("GUI.balance_page.get_account_balance")
def test_load_balance_success(mock_get_balance, qtbot):
    stack = MagicMock()
    mock_get_balance.return_value = (True, 500.0)
    page = BalancePage(stack)
    qtbot.addWidget(page)
    page.load_balance("1234567")
    assert page.account_number == "1234567"
    assert page.balance_label.text() == ("₹500.00")
    mock_get_balance.assert_called_once_with("1234567")


@patch("GUI.balance_page.QMessageBox.warning")
@patch("GUI.balance_page.get_account_balance")
def test_load_balance_failure(mock_get_balance, mock_warning, qtbot):
    stack = MagicMock()
    mock_get_balance.return_value = (False, "Account not found")
    page = BalancePage(stack)
    qtbot.addWidget(page)
    page.load_balance("9999999")
    mock_warning.assert_called_once_with(page, "Balance Error", "Account not found")


def test_balance_back_clicked(qtbot):
    stack = MagicMock()
    page = BalancePage(stack)
    qtbot.addWidget(page)
    page.back_clicked()
    stack.setCurrentIndex.assert_called_once_with(2)
