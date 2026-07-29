from Backend.account_service import get_transaction_history
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,QMessageBox)

class HistoryPage(QWidget):

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_number = None
        self.setup_ui()
    # --------------------------------
    # UI
    # --------------------------------
    def setup_ui(self):
        layout = QVBoxLayout()
        # --------------------------------
        # Title
        # --------------------------------
        title = QLabel("📜 Transaction History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1565C0;
        """)
        # --------------------------------
        # Table
        # --------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Type","Amount","Balance","Time"])
        self.table.horizontalHeader().setStretchLastSection(True)
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
            }""")
        self.back_btn.clicked.connect(self.back_clicked)
        # --------------------------------
        # Add Widgets
        # --------------------------------
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.table)
        layout.addSpacing(20)
        layout.addWidget(
            self.back_btn,
            alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    # --------------------------------
    # Load Transaction History
    # --------------------------------
    def load_history(self, account_number):
        self.account_number = account_number
        success, transactions = get_transaction_history(account_number)
        if not success:
            QMessageBox.warning(
                self,
                "Error",
                transactions
            )
            return
        self.table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(transaction[0]))

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(str(transaction[1])))

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(str(transaction[2])))

            self.table.setItem(row, 3, QTableWidgetItem(transaction[3]))

    def back_clicked(self):
        self.stack.setCurrentIndex(2)
