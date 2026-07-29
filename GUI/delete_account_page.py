from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox,)
from Backend.account_service import delete_account

class DeleteAccountPage(QWidget):

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("DELETE ACCOUNT")
        warning = QLabel(
            "⚠ This action cannot be undone.\n"
            "Deleting your account will permanently remove all your data.")
        password_label = QLabel("Current Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.delete_button = QPushButton("Delete Account")
        self.delete_button.clicked.connect(self.delete_account)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(warning)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def set_account_number(self, account_number):
        self.account_number = account_number

    def delete_account(self):
        password = self.password_input.text()
        reply = QMessageBox.question(
            self,
            "Delete Account",
            "Are you sure you want to delete your account?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)
        if reply == QMessageBox.StandardButton.No:
            return
        success, message = delete_account(self.account_number, password)
        if success:
            QMessageBox.information(self, "Success", message)
            self.password_input.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", message)

    def go_back(self):
        self.password_input.clear()
        self.stack.setCurrentIndex(2)
