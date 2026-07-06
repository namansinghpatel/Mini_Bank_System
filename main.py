import sys
from PyQt6.QtWidgets import (
    QApplication,
    QStackedWidget,
)
from GUI.login_page import LoginPage
from GUI.create_account_page import CreateAccountPage
from GUI.welcome_page import WelcomePage
from GUI.balance_page import BalancePage
app = QApplication(sys.argv)
stack = QStackedWidget()
# --------------------------------
# Create Pages
# --------------------------------
login_page = LoginPage(stack)
create_account_page = CreateAccountPage(stack)
welcome_page = WelcomePage(stack)
balance_page = BalancePage(stack)
# --------------------------------
# Add Pages To Stack
# -------------------------------
stack.addWidget(login_page)
stack.addWidget(create_account_page)
stack.addWidget(welcome_page)
stack.addWidget(balance_page)
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
