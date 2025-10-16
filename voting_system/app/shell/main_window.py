from PyQt6.QtWidgets import QMainWindow
from app.features.login.view import LoginView
from app.features.admin.view import AdminView
from app.features.voter.view import VoterView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Voting System')
        self.setStyleSheet(open('app/core/styles.qss').read())

        # Start with LoginView and small window
        self.login = LoginView(self)
        self.setCentralWidget(self.login)
        self.resize_for_login()

    # ----------------------------
    # Resize presets
    # ----------------------------
    def resize_for_login(self):
        self.setFixedSize(480, 360)

    def resize_for_voter(self):
        self.setFixedSize(600, 400)

    def resize_for_admin(self):
        self.setFixedSize(1000, 720)

    # ----------------------------
    # View switching
    # ----------------------------
    def open_admin(self):
        self.admin = AdminView(self)
        self.setCentralWidget(self.admin)
        self.resize_for_admin()

    def open_voter(self, voter_row):
        self.voter_view = VoterView(self, voter_row)
        self.setCentralWidget(self.voter_view)
        self.resize_for_voter()

    def return_to_login(self):
        self.login = LoginView(self)
        self.setCentralWidget(self.login)
        self.resize_for_login()
