from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget,QLabel,QPushButton,QVBoxLayout,QLineEdit,QMessageBox,)
from Backend.account_service import change_password

class ChangePasswordPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None
        self.setup_ui()

    def setup_ui(self):
        # --------------------------------
        # Main Layout
        # --------------------------------
        layout = QVBoxLayout()
        # --------------------------------
        # Title
        # --------------------------------
        title = QLabel("🔒 Change Password")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1565C0;
        """)
        # --------------------------------
        # Current Password
        # --------------------------------
        current_label = QLabel("Current Password")
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # -------------------------------
        # New Password
        # --------------------------------
        new_label = QLabel("New Password")
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # --------------------------------
        # Confirm Password
        # --------------------------------
        confirm_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # --------------------------------
        # Change Password Button
        # --------------------------------
        self.change_password_btn = QPushButton("Change Password")
        self.change_password_btn.clicked.connect(self.change_password_clicked)
        # --------------------------------
        # Back Button
        # --------------------------------
        self.back_btn = QPushButton("⬅ Back")
        self.back_btn.clicked.connect(self.back_clicked)
        # --------------------------------
        # Button Styling
        # --------------------------------
        buttons = [self.change_password_btn, self.back_btn,]
        for button in buttons:
            button.setMinimumSize(220, 50)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #1565C0;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                }

                QPushButton:hover {
                    background-color: #1E88E5;
                }
            """)
        # --------------------------------
        # Add Widgets
        # --------------------------------
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(current_label)
        layout.addWidget(self.current_password_input)
        layout.addSpacing(15)
        layout.addWidget(new_label)
        layout.addWidget(self.new_password_input)
        layout.addSpacing(15)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(30)
        layout.addWidget(self.change_password_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
    # --------------------------------
    # Set Account
    # --------------------------------
    def set_account(self, account_number):
        self.account_number = account_number
    # --------------------------------
    # Change Password
    # --------------------------------
    def change_password_clicked(self):
        reply = QMessageBox.question(
            self,
            "Change Password",
            "Are you sure you want to change your password?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,)
        if reply == QMessageBox.StandardButton.No:
            return
        success, message = change_password(
            self.account_number,
            self.current_password_input.text(),
            self.new_password_input.text(),
            self.confirm_password_input.text(),)
        if success:
            QMessageBox.information(self, "Success", message)
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", message)
    # --------------------------------
    # Back Button
    # --------------------------------
    def back_clicked(self):
        self.current_password_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        self.stack.setCurrentIndex(2)
