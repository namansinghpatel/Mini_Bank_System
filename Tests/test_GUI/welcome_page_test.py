from GUI.welcome_page import WelcomePage
from unittest.mock import MagicMock


def test_welcome_page_creation(qtbot):
    page = WelcomePage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_check_balance_clicked(qtbot):
    stack = MagicMock()
    balance_page = MagicMock()
    stack.widget.return_value = balance_page
    page = WelcomePage(stack)
    qtbot.addWidget(page)
    page.set_user_details("prashant", "1234567")
    page.check_balance_clicked()
    stack.widget.assert_called_once_with(3)
    balance_page.load_balance.assert_called_once_with("1234567")
    stack.setCurrentIndex.assert_called_once_with(3)


def test_deposit_clicked(qtbot):
    stack = MagicMock()
    deposit_page = MagicMock()
    stack.widget.return_value = deposit_page
    page = WelcomePage(stack)
    qtbot.addWidget(page)
    page.set_user_details("prashant", "1234567")
    page.deposit_clicked()
    stack.widget.assert_called_once_with(4)
    deposit_page.set_account.assert_called_once_with("1234567")
    stack.setCurrentIndex.assert_called_once_with(4)


def test_withdraw_clicked(qtbot):
    # Create a fake stack
    stack = MagicMock()
    # Create a fake WithdrawPage
    withdraw_page = MagicMock()
    # stack.widget(5) should return our fake page
    stack.widget.return_value = withdraw_page
    # Create WelcomePage
    page = WelcomePage(stack)
    qtbot.addWidget(page)
    # Simulate logged-in user
    page.account_number = "1234567"
    # Call the method
    page.withdraw_clicked()
    # Verify the correct page was requested
    stack.widget.assert_called_once_with(5)
    # Verify account number was passed
    withdraw_page.set_account.assert_called_once_with("1234567")
    # Verify page navigation
    stack.setCurrentIndex.assert_called_once_with(5)
