from GUI.login_page import LoginPage


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