from unittest.mock import MagicMock, patch
from GUI.login_page import LoginPage
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit


def test_login_page_creation(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_login_username_field_exists(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page.username is not None


def test_login_password_field_exists(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page.password is not None


@patch("GUI.login_page.login_user")
@patch("GUI.login_page.QMessageBox.information")
def test_login_success(
    mock_information,
    mock_login_user,
    qtbot,
):
    mock_stack = MagicMock()
    mock_login_user.return_value = (
        True,
        {
            "message": "Login Successful",
            "username": "prashant",
            "account_number": "1234567",
        },
    )
    page = LoginPage(mock_stack)
    qtbot.addWidget(page)
    page.username.setText("prashant")
    page.password.setText("password123")
    page.login_clicked()
    mock_information.assert_called_once_with(page, "Success", "Login Successful")
    mock_stack.widget.assert_called_once_with(2)
    mock_stack.widget(2).set_user_details.assert_called_once_with("prashant", "1234567")
    mock_stack.setCurrentIndex.assert_called_once_with(2)


@patch("GUI.login_page.login_user")
@patch("GUI.login_page.QMessageBox.warning")
def test_login_failure(
    mock_warning,
    mock_login_user,
    qtbot,
):
    mock_stack = MagicMock()
    mock_login_user.return_value = (
        False,
        "Invalid Username or Password",
    )
    page = LoginPage(mock_stack)
    qtbot.addWidget(page)
    page.username.setText("prashant")
    page.password.setText("wrongpassword")
    page.login_clicked()
    mock_warning.assert_called_once_with(
        page, "Login Failed", "Invalid Username or Password"
    )
    mock_stack.setCurrentIndex.assert_not_called()


def test_create_account_clicked(qtbot):
    mock_stack = MagicMock()
    page = LoginPage(mock_stack)
    qtbot.addWidget(page)
    page.create_account_clicked()
    mock_stack.setCurrentIndex.assert_called_once_with(1)


@patch("GUI.login_page.QApplication.quit")
def test_exit_application(
    mock_quit,
    qtbot,
):
    page = LoginPage(None)
    qtbot.addWidget(page)
    page.exit_application()
    mock_quit.assert_called_once()


def test_show_password_button_click(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    page.password.setEchoMode(QLineEdit.EchoMode.Password)
    qtbot.mouseClick(page.show_password_btn, Qt.MouseButton.LeftButton)
    assert page.password.echoMode() == QLineEdit.EchoMode.Normal
    assert page.show_password_btn.text() == "🙈"


def test_hide_password_button_click(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    page.password.setEchoMode(QLineEdit.EchoMode.Normal)
    page.show_password_btn.setText("🙈")
    qtbot.mouseClick(page.show_password_btn, Qt.MouseButton.LeftButton)
    assert page.password.echoMode() == QLineEdit.EchoMode.Password
    assert page.show_password_btn.text() == "👁"
