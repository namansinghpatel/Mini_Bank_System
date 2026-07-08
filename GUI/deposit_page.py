from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from Backend.account_service import deposit_money


class DepositPage(QWidget):

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None
        self.setup_ui()

    def setup_ui(self):
        # ----------------------------------
        # Main Layout
        # ----------------------------------
        layout = QVBoxLayout()
        # ----------------------------------
        # Title
        # ----------------------------------
        title = QLabel("💵 Deposit Money")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#1565C0;
        """)
        # ----------------------------------
        # Account Number Label
        # ----------------------------------
        self.account_label = QLabel("Account Number : ")
        self.account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.account_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        # ----------------------------------
        # Amount Label
        # ----------------------------------
        amount_label = QLabel("Enter Amount")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)
        # ----------------------------------
        # Amount Textbox
        # ----------------------------------
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Enter amount")
        self.amount.setFixedWidth(250)
        self.amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # ----------------------------------
        # Deposit Button
        # ----------------------------------
        self.deposit_btn = QPushButton("Deposit")
        self.deposit_btn.setFixedSize(
            220,
            50,
        )
        self.deposit_btn.clicked.connect(self.deposit_clicked)
        # ----------------------------------
        # Back Button
        # ----------------------------------
        self.back_btn = QPushButton("⬅ Back")
        self.back_btn.setFixedSize(
            220,
            50,
        )
        self.back_btn.clicked.connect(self.back_clicked)
        # ----------------------------------
        # Button Style
        # ----------------------------------
        buttons = [
            self.deposit_btn,
            self.back_btn,
        ]
        for button in buttons:
            button.setStyleSheet("""
                QPushButton{
                    background-color:#1565C0;
                    color:white;
                    font-size:16px;
                    font-weight:bold;
                    border-radius:8px;
                }
                QPushButton:hover{
                    background-color:#1E88E5;
                }
            """)
        # ----------------------------------
        # Add Widgets
        # ----------------------------------
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(self.account_label)
        layout.addSpacing(30)
        layout.addWidget(amount_label)
        layout.addWidget(
            self.amount,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addSpacing(30)
        layout.addWidget(
            self.deposit_btn,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addSpacing(15)
        layout.addWidget(
            self.back_btn,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addStretch()
        self.setLayout(layout)
    # ----------------------------------
    # Called from Welcome Page
    # ----------------------------------

    def set_account(self, account_number):
        self.account_number = account_number
        self.account_label.setText(f"🏦 Account Number : {account_number}")
        self.amount.clear()
    # ----------------------------------
    # Deposit Button
    # ----------------------------------

    def deposit_clicked(self):
        amount = self.amount.text()
        success, message = deposit_money(
            self.account_number,
            amount,
        )
        if success:
            QMessageBox.information(
                self,
                "Success",
                message,
            )
            self.amount.clear()
        else:
            QMessageBox.warning(
                self,
                "Deposit Failed",
                message,
            )
    # ----------------------------------
    # Back Button
    # ----------------------------------
    def back_clicked(self):
        self.amount.clear()
        self.stack.setCurrentIndex(2)
