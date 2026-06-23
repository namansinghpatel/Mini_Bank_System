from GUI.welcome_page import WelcomePage


def test_welcome_page_creation(qtbot):
    page = WelcomePage(None)
    qtbot.addWidget(page)
    assert page is not None