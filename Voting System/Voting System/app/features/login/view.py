
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
                             QHBoxLayout, QLabel, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt
from features.items import service as svc
from features.admin.view import AdminWidget
from features.voter.view import VoterWidget

class LoginWidget(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('<b>School Voting System — Login / Register</b>'))

        form = QFormLayout()
        self.student_id = QLineEdit(); self.student_id.setPlaceholderText('student id (for voters)')
        self.name = QLineEdit(); self.name.setPlaceholderText('name (for registration)')
        self.password = QLineEdit(); self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText('password')
        form.addRow('Student ID:', self.student_id)
        form.addRow('Name:', self.name)
        form.addRow('Password:', self.password)
        self.layout.addLayout(form)

        row = QHBoxLayout()
        self.admin_check = QCheckBox('Login as admin')
        row.addWidget(self.admin_check)
        row.addStretch()
        self.login_btn = QPushButton('Login')
        self.register_btn = QPushButton('Register (voter)')
        row.addWidget(self.register_btn)
        row.addWidget(self.login_btn)
        self.layout.addLayout(row)

        # Connect
        self.register_btn.clicked.connect(self.handle_register)
        self.login_btn.clicked.connect(self.handle_login)

    def handle_register(self):
        sid = self.student_id.text().strip()
        name = self.name.text().strip()
        pw = self.password.text().strip()
        if not sid or not name or not pw:
            QMessageBox.warning(self, 'Missing', 'Provide student id, name and password to register.')
            return
        ok = svc.register_voter(sid, name, pw)
        if ok:
            QMessageBox.information(self, 'Registered', 'Registration submitted. Wait for admin verification.')
            self.student_id.clear(); self.name.clear(); self.password.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Registration failed (maybe student id exists).')

    def handle_login(self):
        if self.admin_check.isChecked():
            # Admin login
            username = self.name.text().strip() or 'admin'
            pw = self.password.text().strip() or ''
            if svc.authenticate_admin(username, pw):
                # Load admin tab
                self.parent_window.tabs.addTab(AdminWidget(parent_window=self.parent_window), 'Admin')
                self.parent_window.tabs.setCurrentIndex(self.parent_window.tabs.count() - 1)
            else:
                QMessageBox.critical(self, 'Admin login failed', 'Invalid admin credentials.')
        else:
            sid = self.student_id.text().strip()
            pw = self.password.text().strip()
            user, msg = svc.authenticate_voter(sid, pw)
            if not user:
                QMessageBox.critical(self, 'Login failed', msg)
                return
            # Load voter tab, pass voter id
            voter_tab = VoterWidget(voter=user)
            self.parent_window.tabs.addTab(voter_tab, 'Vote')
            self.parent_window.tabs.setCurrentIndex(self.parent_window.tabs.count() - 1)
