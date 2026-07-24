from unittest.mock import patch
from GUI.transfer_page import TransferPage


def test_transfer_page_creation(qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_set_account(qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)
    page.set_account("1234567")
    assert page.account_number == "1234567"
    assert page.account_label.text() == "1234567"
    assert page.receiver_input.text() == ""
    assert page.amount_input.text() == ""


@patch("GUI.transfer_page.QMessageBox.information")
@patch("GUI.transfer_page.transfer_money")
def test_transfer_success(mock_transfer, mock_information, qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)
    page.account_number = "1001"
    page.receiver_input.setText("1002")
    page.amount_input.setText("300")
    mock_transfer.return_value = (True, "₹300.00 transferred successfully.")
    page.transfer_clicked()
    mock_transfer.assert_called_once_with("1001", "1002", "300")
    mock_information.assert_called_once()
    assert page.receiver_input.text() == ""
    assert page.amount_input.text() == ""


@patch("GUI.transfer_page.QMessageBox.warning")
@patch("GUI.transfer_page.transfer_money")
def test_transfer_failure(mock_transfer, mock_warning, qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)
    page.account_number = "1001"
    page.receiver_input.setText("1002")
    page.amount_input.setText("300")
    mock_transfer.return_value = (False, "Insufficient balance.")
    page.transfer_clicked()
    mock_transfer.assert_called_once_with("1001", "1002", "300")
    mock_warning.assert_called_once()
    assert page.receiver_input.text() == "1002"
    assert page.amount_input.text() == "300"


def test_back_button(qtbot):
    class DummyStack:
        def __init__(self):
            self.index = None

        def setCurrentIndex(self, index):
            self.index = index

    stack = DummyStack()
    page = TransferPage(stack)
    qtbot.addWidget(page)
    page.receiver_input.setText("1002")
    page.amount_input.setText("300")
    page.back_clicked()
    assert stack.index == 2
    assert page.receiver_input.text() == ""
    assert page.amount_input.text() == ""


@patch("GUI.transfer_page.transfer_money")
def test_transfer_button_click(mock_transfer, qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)
    page.account_number = "1001"
    page.receiver_input.setText("1002")
    page.amount_input.setText("300")
    mock_transfer.return_value = (True, "Success")
    page.transfer_btn.click()
    mock_transfer.assert_called_once()
