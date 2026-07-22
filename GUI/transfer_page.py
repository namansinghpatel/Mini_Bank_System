from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,)
from Backend.account_service import transfer_money

class TransferPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None

        self.title_label = QLabel("Transfer Money")
        self.account_title = QLabel("Your Account")
        self.account_label = QLabel("")
        self.receiver_label = QLabel("Receiver Account")
        self.receiver_input = QLineEdit()
        self.amount_label = QLabel("Amount")
        self.amount_input = QLineEdit()
        self.transfer_btn = QPushButton("Transfer")
        self.back_btn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.account_title)
        layout.addWidget(self.account_label)
        layout.addWidget(self.receiver_label)
        layout.addWidget(self.receiver_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.transfer_btn)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

        self.transfer_btn.clicked.connect(self.transfer_clicked)
        self.back_btn.clicked.connect(self.back_clicked)

    def set_account(self, account_number):
        self.account_number = account_number
        self.account_label.setText(account_number)
        self.receiver_input.clear()
        self.amount_input.clear()

    def transfer_clicked(self):
        receiver_account = self.receiver_input.text()
        amount = self.amount_input.text()
        success, message = transfer_money(self.account_number, receiver_account, amount)
        if success:
            QMessageBox.information(self,"Success", message,)
            self.receiver_input.clear()
            self.amount_input.clear()
        else:
            QMessageBox.warning( self, "Error", message, )

    def back_clicked(self):
        self.receiver_input.clear()
        self.amount_input.clear()
        self.stack.setCurrentIndex(2)