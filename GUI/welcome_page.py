from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
)


class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("XYZ Banking System")
        self.setMinimumSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        # ======================================================
        # Main Layout
        # ======================================================
        main_layout = QVBoxLayout()
        # ======================================================
        # Title
        # ======================================================
        title = QLabel("🏦 Welcome To XYZ Banking System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#1565C0;
            margin-top:20px;
            margin-bottom:20px;
        """)
        # ======================================================
        # Username Label
        # ======================================================
        self.username_label = QLabel("👤 Username : ")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        # ======================================================
        # Account Number Label
        # ======================================================
        self.account_number_label = QLabel("🏦 Account Number : ")
        self.account_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.account_number_label.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        # ======================================================
        # Button Grid
        # ======================================================
        grid = QGridLayout()
        self.check_balance_btn = QPushButton("💰 Check Balance")
        self.deposit_btn = QPushButton("💵 Deposit")
        self.withdraw_btn = QPushButton("💸 Withdraw")
        self.transfer_btn = QPushButton("🔄 Transfer")
        buttons = [
            self.check_balance_btn,
            self.deposit_btn,
            self.withdraw_btn,
            self.transfer_btn,
        ]
        for button in buttons:
            button.setMinimumSize(220, 80)
            button.setStyleSheet("""
                QPushButton{
                    background-color:#1565C0;
                    color:white;
                    font-size:16px;
                    font-weight:bold;
                    border-radius:10px;
                }
                QPushButton:hover{
                    background-color:#1E88E5;
                }
            """)
        grid.addWidget(
            self.check_balance_btn,
            0,
            0,
        )
        grid.addWidget(
            self.deposit_btn,
            0,
            1,
        )
        grid.addWidget(
            self.withdraw_btn,
            1,
            0,
        )
        grid.addWidget(
            self.transfer_btn,
            1,
            1,
        )
        grid.setHorizontalSpacing(25)
        grid.setVerticalSpacing(25)
        # ======================================================
        # Add Widgets
        # ======================================================
        main_layout.addWidget(title)
        main_layout.addWidget(self.username_label)
        main_layout.addWidget(self.account_number_label)
        main_layout.addStretch()
        main_layout.addLayout(grid)
        main_layout.addStretch()
        self.setLayout(main_layout)
    # ==========================================================
    # Update User Information
    # ==========================================================
    def set_user_details(
        self,
        username,
        account_number,
    ):
        self.username_label.setText(f"👤 Username : {username}")
        self.account_number_label.setText(f"🏦 Account Number : {account_number}")
