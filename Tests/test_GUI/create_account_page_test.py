from GUI.create_account_page import CreateAccountPage


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
