from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from Backend.auth_service import create_user
from pathlib import Path


class CreateAccountPage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        # --------------------------------
        # Background Image
        # --------------------------------

        project_root = Path(__file__).resolve().parent.parent

        background_path = (
            project_root
            / "Docs"
            / "Images"
            / "GUI"
            / "bank_background.png"
        )

        self.background_label = QLabel(self)

        self.background_pixmap = QPixmap(
            str(background_path)
        )

        self.background_label.setPixmap(
            self.background_pixmap
        )

        self.background_label.setScaledContents(False)

        # Put background behind all other widgets
        self.background_label.lower()

        # --------------------------------
        # Main Page Layout
        # --------------------------------

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30,
            20,
            30,
            20
        )

        # --------------------------------
        # Bank Title
        # --------------------------------

        title = QLabel(
            "🏦 XYZ Banking System"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                padding: 10px;
                background-color: rgba(0, 0, 0, 80);
                border-radius: 8px;
            }
        """)

        # --------------------------------
        # Create Account Card
        # --------------------------------

        account_card = QFrame()

        account_card.setFixedWidth(380)

        account_card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 240);
                border: 1px solid #D0D7DE;
                border-radius: 15px;
            }
        """)

        # --------------------------------
        # Card Layout
        # --------------------------------

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            35,
            30,
            35,
            30
        )

        card_layout.setSpacing(15)

        account_card.setLayout(
            card_layout
        )

        # --------------------------------
        # Card Title
        # --------------------------------

        account_title = QLabel(
            "Create New Account"
        )

        account_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        account_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1565C0;
                border: none;
                background: transparent;
            }
        """)

        # --------------------------------
        # Username Label
        # --------------------------------

        username_label = QLabel(
            "Username"
        )

        username_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: none;
                background: transparent;
            }
        """)

        # --------------------------------
        # Username Input
        # --------------------------------

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Enter your username"
        )

        self.username.setFixedHeight(
            42
        )

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

        password_label = QLabel(
            "Password"
        )

        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: none;
                background: transparent;
            }
        """)

        # --------------------------------
        # Password Input
        # --------------------------------

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Enter your password"
        )

        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.password.setFixedHeight(
            42
        )

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

        self.show_password_btn = QPushButton(
            "👁"
        )

        self.show_password_btn.setFixedSize(
            42,
            42
        )

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

        password_layout.addWidget(
            self.password
        )

        password_layout.addWidget(
            self.show_password_btn
        )

        # --------------------------------
        # Confirm Password Label
        # --------------------------------

        repassword_label = QLabel(
            "Confirm Password"
        )

        repassword_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: none;
                background: transparent;
            }
        """)

        # --------------------------------
        # Confirm Password Input
        # --------------------------------

        self.repassword = QLineEdit()

        self.repassword.setPlaceholderText(
            "Re-enter your password"
        )

        self.repassword.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.repassword.setFixedHeight(
            42
        )

        self.repassword.setStyleSheet("""
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
        # Submit Button
        # --------------------------------

        submit_btn = QPushButton(
            "Create Account"
        )

        submit_btn.setFixedHeight(
            45
        )

        submit_btn.setStyleSheet("""
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

        submit_btn.clicked.connect(
            self.submit_clicked
        )

        # --------------------------------
        # Back Button
        # --------------------------------

        back_btn = QPushButton(
            "⬅ Back to Login"
        )

        back_btn.setFixedHeight(
            40
        )

        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1565C0;
                border: 1px solid #1565C0;
                border-radius: 7px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)

        back_btn.clicked.connect(
            self.back_clicked
        )

        # --------------------------------
        # Add Widgets To Card
        # --------------------------------

        card_layout.addWidget(
            account_title
        )

        card_layout.addSpacing(
            10
        )

        card_layout.addWidget(
            username_label
        )

        card_layout.addWidget(
            self.username
        )

        card_layout.addWidget(
            password_label
        )

        card_layout.addLayout(
            password_layout
        )

        card_layout.addWidget(
            repassword_label
        )

        card_layout.addWidget(
            self.repassword
        )

        card_layout.addSpacing(
            10
        )

        card_layout.addWidget(
            submit_btn
        )

        card_layout.addWidget(
            back_btn
        )

        # --------------------------------
        # Main Page Layout
        # --------------------------------

        main_layout.addWidget(
            title
        )

        main_layout.addStretch()

        main_layout.addWidget(
            account_card,
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
                color: white;
                font-size: 12px;
                padding: 8px;
                background-color: rgba(0, 0, 0, 80);
                border-radius: 5px;
            }
        """)

        main_layout.addWidget(
            footer
        )

        # --------------------------------
        # Set Main Layout
        # --------------------------------

        self.setLayout(
            main_layout
        )

        # --------------------------------
        # Page Background
        # --------------------------------

        self.setStyleSheet("""
            CreateAccountPage {
                background-color: #263238;
            }
        """)

    # --------------------------------
    # Resize Background Image
    # --------------------------------

    def resizeEvent(self, event):

        if not self.background_pixmap.isNull():

            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            self.background_label.setPixmap(
                scaled_pixmap
            )

            self.background_label.setGeometry(
                self.rect()
            )

        super().resizeEvent(event)

    # --------------------------------
    # Submit
    # --------------------------------

    def submit_clicked(self):

        username = self.username.text()

        password = self.password.text()

        re_password = self.repassword.text()

        success, message = create_user(
            username,
            password,
            re_password
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                message
            )

            self.stack.setCurrentIndex(0)

        else:

            QMessageBox.warning(
                self,
                "Validation Error",
                message
            )

    # --------------------------------
    # Back Button
    # --------------------------------

    def back_clicked(self):

        self.stack.setCurrentIndex(0)

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

            self.show_password_btn.setText(
                "🙈"
            )

        else:

            self.password.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.show_password_btn.setText(
                "👁"
            )