from GUI.create_account_page import CreateAccountPage
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit


def test_create_account_page_creation(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_create_account_username_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.username is not None


def test_create_account_password_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.password is not None


def test_create_account_repassword_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.repassword is not None


from unittest.mock import MagicMock


def test_back_button(qtbot):

    mock_stack = MagicMock()

    page = CreateAccountPage(mock_stack)

    qtbot.addWidget(page)

    page.back_clicked()

    mock_stack.setCurrentIndex.assert_called_once_with(0)


from unittest.mock import patch


@patch("GUI.create_account_page.create_user")
@patch("GUI.create_account_page.QMessageBox.information")
def test_submit_clicked_success(mock_messagebox, mock_create_user, qtbot):

    mock_stack = MagicMock()

    mock_create_user.return_value = (True, "Account Created Successfully")

    page = CreateAccountPage(mock_stack)

    qtbot.addWidget(page)

    page.username.setText("prashant")

    page.password.setText("password123")

    page.repassword.setText("password123")

    page.submit_clicked()

    mock_messagebox.assert_called_once()

    mock_stack.setCurrentIndex.assert_called_once_with(0)


@patch("GUI.create_account_page.create_user")
@patch("GUI.create_account_page.QMessageBox.warning")
def test_submit_clicked_failure(mock_warning, mock_create_user, qtbot):
    mock_create_user.return_value = (False, "Passwords do not match")
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    page.username.setText("prashant")
    page.password.setText("123")
    page.repassword.setText("456")
    page.submit_clicked()
    mock_warning.assert_called_once()


def test_show_password_button_click(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    page.password.setEchoMode(QLineEdit.EchoMode.Password)
    qtbot.mouseClick(page.show_password_btn, Qt.MouseButton.LeftButton)
    assert page.password.echoMode() == QLineEdit.EchoMode.Normal


def test_hide_password_button_click(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    page.password.setEchoMode(QLineEdit.EchoMode.Normal)
    page.show_password_btn.setText("🙈")
    qtbot.mouseClick(page.show_password_btn, Qt.MouseButton.LeftButton)
    assert page.password.echoMode() == QLineEdit.EchoMode.Password
