from unittest.mock import MagicMock, patch
from GUI.change_password_page import ChangePasswordPage
from PyQt6.QtWidgets import QStackedWidget

from unittest.mock import patch
from PyQt6.QtWidgets import QStackedWidget, QWidget, QMessageBox


@patch("GUI.change_password_page.QMessageBox.question")
@patch("GUI.change_password_page.change_password")
def test_change_password_button_click(
    mock_change_password,
    mock_question,
    qtbot,):
    stack = QStackedWidget()
    # Dummy Login Page (Index 0)
    stack.addWidget(QWidget())
    page = ChangePasswordPage(stack)
    qtbot.addWidget(page)
    stack.addWidget(page)
    page.account_number = "1001"
    page.current_password_input.setText("OldPassword123")
    page.new_password_input.setText("NewPassword123")
    page.confirm_password_input.setText("NewPassword123")
    mock_question.return_value = QMessageBox.StandardButton.Yes
    mock_change_password.return_value = (
        True,
        "Password changed successfully.",)
    page.change_password_clicked()
    mock_change_password.assert_called_once_with(
        "1001",
        "OldPassword123",
        "NewPassword123",
        "NewPassword123")
    assert stack.currentIndex() == 0


def test_set_account(qtbot):
    page = ChangePasswordPage(None)
    qtbot.addWidget(page)
    page.set_account("1001")
    assert page.account_number == "1001"


def test_password_fields(qtbot):
    page = ChangePasswordPage(None)
    qtbot.addWidget(page)
    page.current_password_input.setText("OldPassword123")
    page.new_password_input.setText("NewPassword123")
    page.confirm_password_input.setText("NewPassword123")
    assert page.current_password_input.text() == "OldPassword123"
    assert page.new_password_input.text() == "NewPassword123"
    assert page.confirm_password_input.text() == "NewPassword123"


def test_back_button(qtbot):
    stack = QStackedWidget()
    # Dummy Pages
    stack.addWidget(QWidget())      # Index 0
    stack.addWidget(QWidget())      # Index 1
    page = ChangePasswordPage(stack)
    qtbot.addWidget(page)
    stack.addWidget(page)           # Index 2
    stack.setCurrentIndex(2)
    page.back_clicked()
    assert stack.currentIndex() == 2


