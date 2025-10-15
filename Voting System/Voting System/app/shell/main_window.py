
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from features.login.view import LoginWidget
from core.utils import load_stylesheet

def run_app():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont('Segoe UI', 10))
    app.setStyleSheet(load_stylesheet('app/core/styless.qss'))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('School Voting System')
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        # Start with only login tab; other tabs are added after login
        self.login_tab = LoginWidget(parent_window=self)
        self.tabs.addTab(self.login_tab, 'Login / Register')

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.tabs)
        self.setCentralWidget(container)
