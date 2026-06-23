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