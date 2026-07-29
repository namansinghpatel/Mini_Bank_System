from unittest.mock import patch
from GUI.history_page import HistoryPage
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QStackedWidget


@patch("GUI.history_page.get_transaction_history")
def test_load_history_success(mock_history, qtbot):
    page = HistoryPage(None)
    qtbot.addWidget(page)

    mock_history.return_value = (
        True,
        [("Deposit", 500, 500, "2026-07-27 10:00:00")])

    page.load_history("1001")
    mock_history.assert_called_once_with("1001")
    assert page.table.rowCount() == 1
    assert page.table.item(0, 0).text() == "Deposit"
    assert page.table.item(0, 1).text() == "500"
    assert page.table.item(0, 2).text() == "500"
    assert page.table.item(0, 3).text() == "2026-07-27 10:00:00"


@patch("GUI.history_page.get_transaction_history")
def test_load_empty_history(mock_history, qtbot):
    page = HistoryPage(None)
    qtbot.addWidget(page)
    mock_history.return_value = (True, [])
    page.load_history("1001")
    mock_history.assert_called_once_with("1001")
    assert page.table.rowCount() == 0


@patch("GUI.history_page.get_transaction_history")
def test_load_history_failure(mock_history, qtbot):
    page = HistoryPage(None)
    qtbot.addWidget(page)
    mock_history.return_value = (False, "Account not found.")
    page.load_history("9999")
    mock_history.assert_called_once_with("9999")


@patch("GUI.history_page.get_transaction_history")
def test_table_headers(mock_history, qtbot):
    page = HistoryPage(None)
    qtbot.addWidget(page)
    mock_history.return_value = (True, [])
    page.load_history("1001")
    assert page.table.horizontalHeaderItem(0).text() == "Type"
    assert page.table.horizontalHeaderItem(1).text() == "Amount"
    assert page.table.horizontalHeaderItem(2).text() == "Balance"
    assert page.table.horizontalHeaderItem(3).text() == "Time"


def test_back_button(qtbot):
    stack = QStackedWidget()
    page = HistoryPage(stack)
    qtbot.addWidget(stack)
    qtbot.addWidget(page)
    page.back_btn.click()