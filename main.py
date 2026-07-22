import sys
from PyQt6.QtWidgets import (
    QApplication,
    QStackedWidget,
)
from GUI.login_page import LoginPage
from GUI.create_account_page import CreateAccountPage
from GUI.welcome_page import WelcomePage
from GUI.balance_page import BalancePage
from GUI.deposit_page import DepositPage
from GUI.withdraw_page import WithdrawPage
from GUI.transfer_page import TransferPage
app = QApplication(sys.argv)
stack = QStackedWidget()
# --------------------------------
# Create Pages
# --------------------------------
login_page = LoginPage(stack)
create_account_page = CreateAccountPage(stack)
welcome_page = WelcomePage(stack)
balance_page = BalancePage(stack)
deposit_page = DepositPage(stack)
withdraw_page = WithdrawPage(stack)
transfer_page = TransferPage(stack)
# --------------------------------
# Add Pages To Stack
# -------------------------------
stack.addWidget(login_page)
stack.addWidget(create_account_page)
stack.addWidget(welcome_page)
stack.addWidget(balance_page)
stack.addWidget(deposit_page)
stack.addWidget(withdraw_page)
stack.addWidget(transfer_page)
# --------------------------------
# Window Settings
# --------------------------------
stack.setWindowTitle("XYZ Banking System")
stack.setMinimumSize(
    800,
    600,
)
stack.setCurrentIndex(0)
stack.show()
sys.exit(app.exec())
