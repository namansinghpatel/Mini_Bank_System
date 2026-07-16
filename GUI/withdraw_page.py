from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
)
from Backend.account_service import withdraw_money


class WithdrawPage(QWidget):

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None
        self.setWindowTitle("Withdraw Money")
        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):
        layout = QVBoxLayout()
        # ------------------------------------------
        # Title
        # ------------------------------------------

        title = QLabel("💸 Withdraw Money")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1565C0;
            margin-bottom:20px;
        """)
        # ------------------------------------------
        # Account Number
        # ------------------------------------------
        self.account_label = QLabel("🏦 Account Number : ")
        self.account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.account_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        # ------------------------------------------
        # Amount
        # ------------------------------------------
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Enter amount to withdraw")
        # ------------------------------------------
        # Buttons
        # ------------------------------------------
        self.withdraw_btn = QPushButton("Withdraw")
        self.back_btn = QPushButton("Back")
        self.withdraw_btn.clicked.connect(self.withdraw_clicked)
        self.back_btn.clicked.connect(self.back_clicked)
        # ------------------------------------------
        # Layout
        # ------------------------------------------
        layout.addWidget(title)
        layout.addWidget(self.account_label)
        layout.addWidget(self.amount)
        layout.addWidget(self.withdraw_btn)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    # =====================================================
    # Receive Logged-in Account
    # =====================================================

    def set_account(self, account_number):
        self.account_number = account_number
        self.account_label.setText(f"🏦 Account Number : {account_number}")
        self.amount.clear()

    # =====================================================
    # Withdraw Button
    # =====================================================

    def withdraw_clicked(self):
        amount = self.amount.text()
        success, message = withdraw_money(self.account_number, amount)
        if success:
            QMessageBox.information(self, "Success", message)
            self.amount.clear()
        else:
            QMessageBox.warning(self, "Withdrawal Failed", message)

    # =====================================================
    # Back Button
    # =====================================================

    def back_clicked(self):
        self.amount.clear()
        self.stack.setCurrentIndex(2)
