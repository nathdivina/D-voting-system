from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from app.features.login.service import register_voter, login_voter

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Admin@123456'

class LoginView(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle('Login')
        self.setFixedSize(480, 360)
        self.setStyleSheet(open('app/core/styles.qss').read())

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setStyleSheet("""
            QFrame#loginCard {
                background-color: #1e1e1e;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #3c3c3c;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        title = QLabel('Voting System')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        self.identifier = QLineEdit()
        self.identifier.setPlaceholderText('Voter ID or Last Name')
        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        card_layout.addWidget(self.identifier)
        card_layout.addWidget(self.password)

        btn_row = QHBoxLayout()
        self.voter_login_btn = QPushButton('Login as Voter')
        self.admin_login_btn = QPushButton('Login as Admin')
        self.register_btn = QPushButton('Register')

        btn_row.addWidget(self.voter_login_btn)
        btn_row.addWidget(self.admin_login_btn)
        btn_row.addWidget(self.register_btn)
        card_layout.addLayout(btn_row)

        outer_layout.addWidget(card)

        self.voter_login_btn.clicked.connect(self.login_voter)
        self.admin_login_btn.clicked.connect(self.login_admin)
        self.register_btn.clicked.connect(self.register)

    def login_voter(self):
        identifier = self.identifier.text()
        pw = self.password.text()
        user = login_voter(identifier, pw)
        if user:
            QMessageBox.information(self, 'Success', 'Login successful.')
            self.parent_window.open_voter(user)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials or not verified.')

    def login_admin(self):
        uname = self.identifier.text().strip()
        pw = self.password.text().strip()
        if uname == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            QMessageBox.information(self, 'Admin', 'Admin login successful.')
            self.parent_window.open_admin()
        else:
            QMessageBox.warning(self, 'Admin', 'Invalid admin credentials.')

    def register(self):
        from PyQt6.QtWidgets import QInputDialog
        fname, ok = QInputDialog.getText(self, 'Register', 'First name:')
        if not ok or not fname.strip():
            return
        mname, ok = QInputDialog.getText(self, 'Register', 'Middle name (optional):')
        if not ok:
            mname = ''
        lname, ok = QInputDialog.getText(self, 'Register', 'Last name:')
        if not ok or not lname.strip():
            return
        pw, ok = QInputDialog.getText(self, 'Register', 'Password:', QLineEdit.EchoMode.Password)
        if not ok or not pw:
            return

        voter_id, err = register_voter(fname, mname, lname, pw)
        if err:
            QMessageBox.warning(self, 'Invalid Password', err)
        else:
            QMessageBox.information(
                self,
                'Registered',
                f'Registration successful!\n\nYour unique Voter ID is:\n\n🔹 {voter_id}\n\nWait for verification before login.'
            )
