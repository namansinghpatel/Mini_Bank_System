from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
    QApplication,
    QHBoxLayout,
    QFrame,
)
from PyQt6.QtCore import Qt
from Backend.auth_service import login_user


class LoginPage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        # --------------------------------
        # Main Page Layout
        # --------------------------------

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)

        # --------------------------------
        # Bank Title
        # --------------------------------

        title = QLabel("🏦 XYZ Banking System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #1565C0;
                padding: 10px;
            }
        """)

        # --------------------------------
        # Login Card
        # --------------------------------

        login_card = QFrame()
        login_card.setFixedWidth(380)

        login_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #D0D7DE;
                border-radius: 15px;
            }
        """)

        # --------------------------------
        # Card Layout
        # --------------------------------

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(35, 30, 35, 30)
        card_layout.setSpacing(15)

        login_card.setLayout(card_layout)

        # --------------------------------
        # Login Title
        # --------------------------------

        login_title = QLabel("Welcome Back")

        login_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        login_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1565C0;
                border: none;
            }
        """)

        # --------------------------------
        # Username Label
        # --------------------------------

        username_label = QLabel("Username")

        username_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: none;
            }
        """)

        # --------------------------------
        # Username Input
        # --------------------------------

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setFixedHeight(42)

        self.username.setStyleSheet("""
            QLineEdit {
                border: 1px solid #B0BEC5;
                border-radius: 7px;
                padding: 8px;
                font-size: 15px;
                background-color: white;
            }

            QLineEdit:focus {
                border: 2px solid #1565C0;
            }
        """)

        # --------------------------------
        # Password Label
        # --------------------------------

        password_label = QLabel("Password")

        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: none;
            }
        """)

        # --------------------------------
        # Password Input
        # --------------------------------

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.password.setFixedHeight(42)

        self.password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #B0BEC5;
                border-radius: 7px;
                padding: 8px;
                font-size: 15px;
                background-color: white;
            }

            QLineEdit:focus {
                border: 2px solid #1565C0;
            }
        """)

        # --------------------------------
        # Show Password Button
        # --------------------------------

        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setFixedSize(42, 42)

        self.show_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #ECEFF1;
                border: 1px solid #B0BEC5;
                border-radius: 7px;
                font-size: 17px;
            }

            QPushButton:hover {
                background-color: #CFD8DC;
            }
        """)

        self.show_password_btn.clicked.connect(
            self.toggle_password
        )

        # --------------------------------
        # Password Layout
        # --------------------------------

        password_layout = QHBoxLayout()
        password_layout.setSpacing(6)

        password_layout.addWidget(self.password)
        password_layout.addWidget(
            self.show_password_btn
        )

        # --------------------------------
        # Login Button
        # --------------------------------

        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(45)

        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1565C0;
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1E88E5;
            }

            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

        login_btn.clicked.connect(
            self.login_clicked
        )

        # --------------------------------
        # Create Account Button
        # --------------------------------

        create_btn = QPushButton(
            "Create New Account"
        )

        create_btn.setFixedHeight(42)

        create_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1565C0;
                border: 1px solid #1565C0;
                border-radius: 7px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)

        create_btn.clicked.connect(
            self.create_account_clicked
        )

        # --------------------------------
        # Exit Button
        # --------------------------------

        exit_btn = QPushButton("❌ Exit")

        exit_btn.setFixedHeight(40)

        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #757575;
                border: none;
                font-size: 14px;
            }

            QPushButton:hover {
                color: #D32F2F;
            }
        """)

        exit_btn.clicked.connect(
            self.exit_application
        )

        # --------------------------------
        # Add Widgets To Card
        # --------------------------------

        card_layout.addWidget(login_title)

        card_layout.addSpacing(10)

        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username)

        card_layout.addWidget(password_label)
        card_layout.addLayout(password_layout)

        card_layout.addSpacing(10)

        card_layout.addWidget(login_btn)
        card_layout.addWidget(create_btn)
        card_layout.addWidget(exit_btn)

        # --------------------------------
        # Main Page Layout
        # --------------------------------

        main_layout.addWidget(title)

        main_layout.addStretch()

        main_layout.addWidget(
            login_card,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addStretch()

        # --------------------------------
        # Footer
        # --------------------------------

        footer = QLabel(
            "Secure Banking • XYZ Bank"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet("""
            QLabel {
                color: #78909C;
                font-size: 12px;
                padding: 8px;
            }
        """)

        main_layout.addWidget(footer)

        # --------------------------------
        # Set Main Layout
        # --------------------------------

        self.setLayout(main_layout)

        # --------------------------------
        # Page Background
        # --------------------------------

        self.setStyleSheet("""
            LoginPage {
                background-color: #F5F7FA;
            }
        """)

    # --------------------------------
    # Login
    # --------------------------------

    def login_clicked(self):

        username = self.username.text()
        password = self.password.text()

        success, result = login_user(
            username,
            password
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                result["message"]
            )

            # Get Welcome Page
            welcome_page = self.stack.widget(2)

            # Pass logged-in user details
            welcome_page.set_user_details(
                result["username"],
                result["account_number"]
            )

            # Open Welcome Page
            self.stack.setCurrentIndex(2)

        else:

            QMessageBox.warning(
                self,
                "Login Failed",
                result
            )

    # --------------------------------
    # Create Account
    # --------------------------------

    def create_account_clicked(self):

        self.stack.setCurrentIndex(1)

    # --------------------------------
    # Exit Application
    # --------------------------------

    def exit_application(self):

        QApplication.quit()

    # --------------------------------
    # Toggle Password
    # --------------------------------

    def toggle_password(self):

        if (
            self.password.echoMode()
            == QLineEdit.EchoMode.Password
        ):

            self.password.setEchoMode(
                QLineEdit.EchoMode.Normal
            )

            self.show_password_btn.setText("🙈")

        else:

            self.password.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.show_password_btn.setText("👁")