from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from Backend.account_service import get_account_balance


class BalancePage(QWidget):

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
        title = QLabel("💰 Account Balance")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1565C0;
        """)
        # --------------------------------
        # Balance Label
        # --------------------------------
        self.balance_label = QLabel("₹0.00")
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
        """)
        # --------------------------------
        # Back Button
        # --------------------------------
        self.back_btn = QPushButton("⬅ Back")
        self.back_btn.setMinimumSize(200, 50)
        self.back_btn.setStyleSheet("""
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
        self.back_btn.clicked.connect(self.back_clicked)
        # --------------------------------
        # Add Widgets
        # --------------------------------
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(self.balance_label)
        layout.addSpacing(50)
        layout.addWidget(
            self.back_btn,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addStretch()
        self.setLayout(layout)

    # --------------------------------
    # Load Balance
    # --------------------------------

    def load_balance(self, account_number):
        self.account_number = account_number
        success, result = get_account_balance(account_number)
        if success:
            self.balance_label.setText(f"₹{result:.2f}")
        else:
            QMessageBox.warning(self, "Balance Error", result)

    # --------------------------------
    # Back Button
    # --------------------------------

    def back_clicked(self):
        self.stack.setCurrentIndex(2)
