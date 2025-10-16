from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from app.core.db import get_connection, log_history


class VoterView(QWidget):
    def __init__(self, parent=None, voter_row=None):
        super().__init__(parent)
        self.parent = parent
        self.voter = voter_row
        self.conn = get_connection()
        self.selected_votes = {}
        self.setup_ui()

    def setup_ui(self):
        # --- Layout setup ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(10)

        # --- Header ---
        title = QLabel("🗳️ Voting Panel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 8px;")
        main_layout.addWidget(title)

        # --- Scrollable area for positions/candidates ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # --- Load candidate positions dynamically ---
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT position FROM candidates ORDER BY position ASC")
        positions = [r[0] for r in cur.fetchall()]

        for position in positions:
            frame = self.create_position_box(position)
            scroll_layout.addWidget(frame)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # --- Buttons ---
        btn_row = QHBoxLayout()
        self.submit_btn = QPushButton("✅ Submit Votes")
        self.submit_btn.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.submit_btn.clicked.connect(self.submit_votes)

        self.logout_btn = QPushButton("← Back to Login")
        self.logout_btn.setStyleSheet("background-color: #c62828; color: white; font-weight: bold;")
        self.logout_btn.clicked.connect(self.return_to_login)

        btn_row.addWidget(self.submit_btn)
        btn_row.addWidget(self.logout_btn)

        main_layout.addLayout(btn_row)

    # =====================================================
    #   Create candidate table per position
    # =====================================================
    def create_position_box(self, position):
        """Creates a frame with candidates for a specific position"""
        box = QFrame()
        layout = QVBoxLayout(box)
        layout.setSpacing(6)

        label = QLabel(position)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Candidate ID", "Name"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setMinimumHeight(180)  # fits about 5 rows nicely
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM candidates WHERE position = ?", (position,))
        rows = cur.fetchall()
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(str(val)))

        layout.addWidget(table)
        self.selected_votes[position] = table
        return box

    # =====================================================
    #   Voting Logic
    # =====================================================
    def submit_votes(self):
        """Save selected votes to the database and return to login."""
        cur = self.conn.cursor()

        voter_id = self.voter[0] if self.voter else None
        if not voter_id:
            QMessageBox.warning(self, "Error", "Invalid voter data.")
            return

        for position, table in self.selected_votes.items():
            row = table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Incomplete", f"Please select a candidate for '{position}'.")
                return
            candidate_id = int(table.item(row, 0).text())

            cur.execute("UPDATE candidates SET votes = votes + 1 WHERE id = ?", (candidate_id,))

        self.conn.commit()
        log_history("Vote Cast", f"Voter ID {voter_id} submitted their votes.")

        QMessageBox.information(self, "Vote Submitted", "Your votes have been recorded successfully!")
        self.return_to_login()

    def return_to_login(self):
        """Return to login screen after voting or logout."""
        if self.parent:
            self.parent.return_to_login()
