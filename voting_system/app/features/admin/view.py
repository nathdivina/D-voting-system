from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QScrollArea, QFrame,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from app.features.admin.service import (
    get_unverified_voters, verify_voter,
    get_candidates, create_candidate, edit_candidate, remove_candidate,
    get_history_records
)
from app.core.db import log_history, get_connection


class AdminView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # === Main layout ===
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(10)

        # ---- Header ----
        header = QLabel("🧑‍💼 Admin Dashboard")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(header)

        # ---- Scrollable area ----
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(25)

        # ---------------------------
        #  UNVERIFIED VOTERS SECTION
        # ---------------------------
        voter_label = QLabel("Unverified Voters")
        voter_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.voters_table = QTableWidget()
        self.voters_table.setMinimumHeight(240)
        self.voters_table.setMaximumHeight(240)
        self.voters_table.setColumnCount(4)
        self.voters_table.setHorizontalHeaderLabels(["DB ID", "Student ID", "Full Name", "Hashed Password"])
        self.voters_table.horizontalHeader().setStretchLastSection(True)
        for i in range(4):
            self.voters_table.horizontalHeader().setSectionResizeMode(
                i, self.voters_table.horizontalHeader().ResizeMode.Stretch
            )

        voter_btn_row = QHBoxLayout()
        self.verify_btn = QPushButton("✅ Verify Selected")
        self.verify_btn.clicked.connect(self.verify_voter)
        self.refresh_voters_btn = QPushButton("🔄 Refresh Voters")
        self.refresh_voters_btn.clicked.connect(self.load_voters)
        voter_btn_row.addWidget(self.verify_btn)
        voter_btn_row.addWidget(self.refresh_voters_btn)

        voter_box = QVBoxLayout()
        voter_box.addWidget(voter_label)
        voter_box.addWidget(self.voters_table)
        voter_box.addLayout(voter_btn_row)

        vframe = QFrame()
        vframe.setLayout(voter_box)
        scroll_layout.addWidget(vframe)

        # ---------------------------
        #  CANDIDATE MANAGEMENT
        # ---------------------------
        cand_label = QLabel("Candidates & Positions")
        cand_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.candidates_table = QTableWidget()
        self.candidates_table.setMinimumHeight(240)
        self.candidates_table.setMaximumHeight(240)
        self.candidates_table.setColumnCount(3)
        self.candidates_table.setHorizontalHeaderLabels(["ID", "Position", "Name"])
        self.candidates_table.horizontalHeader().setStretchLastSection(True)
        for i in range(3):
            self.candidates_table.horizontalHeader().setSectionResizeMode(
                i, self.candidates_table.horizontalHeader().ResizeMode.Stretch
            )

        cand_btn_row = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add")
        self.edit_btn = QPushButton("✏️ Edit")
        self.delete_btn = QPushButton("🗑️ Delete")
        self.refresh_cand_btn = QPushButton("🔄 Refresh")

        self.add_btn.clicked.connect(self.add_candidate)
        self.edit_btn.clicked.connect(self.edit_candidate)
        self.delete_btn.clicked.connect(self.delete_candidate)
        self.refresh_cand_btn.clicked.connect(self.load_candidates)

        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_cand_btn]:
            cand_btn_row.addWidget(btn)

        cand_box = QVBoxLayout()
        cand_box.addWidget(cand_label)
        cand_box.addWidget(self.candidates_table)
        cand_box.addLayout(cand_btn_row)

        cframe = QFrame()
        cframe.setLayout(cand_box)
        scroll_layout.addWidget(cframe)

        # ---------------------------
        #  VOTE OVERVIEW SECTION
        # ---------------------------
        votes_label = QLabel("Votes Overview")
        votes_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.votes_table = QTableWidget()
        self.votes_table.setMinimumHeight(240)
        self.votes_table.setMaximumHeight(240)
        self.votes_table.setColumnCount(3)
        self.votes_table.setHorizontalHeaderLabels(["Position", "Candidate Name", "Total Votes"])
        self.votes_table.horizontalHeader().setStretchLastSection(True)
        for i in range(3):
            self.votes_table.horizontalHeader().setSectionResizeMode(
                i, self.votes_table.horizontalHeader().ResizeMode.Stretch
            )

        refresh_votes_btn = QPushButton("🔄 Refresh Votes")
        refresh_votes_btn.clicked.connect(self.load_votes)

        vbox = QVBoxLayout()
        vbox.addWidget(votes_label)
        vbox.addWidget(self.votes_table)
        vbox.addWidget(refresh_votes_btn)

        vframe2 = QFrame()
        vframe2.setLayout(vbox)
        scroll_layout.addWidget(vframe2)

        # ---------------------------
        #  HISTORY SECTION
        # ---------------------------
        history_label = QLabel("System History")
        history_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.history_table = QTableWidget()
        self.history_table.setMinimumHeight(240)
        self.history_table.setMaximumHeight(240)
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Action", "Details", "Timestamp"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        for i in range(3):
            self.history_table.horizontalHeader().setSectionResizeMode(
                i, self.history_table.horizontalHeader().ResizeMode.Stretch
            )

        refresh_history_btn = QPushButton("🔄 Refresh History")
        refresh_history_btn.clicked.connect(self.load_history)

        hbox = QVBoxLayout()
        hbox.addWidget(history_label)
        hbox.addWidget(self.history_table)
        hbox.addWidget(refresh_history_btn)

        hframe = QFrame()
        hframe.setLayout(hbox)
        scroll_layout.addWidget(hframe)

        # ---- Scrollable content ----
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # ---- Logout ----
        self.back_btn = QPushButton("← Logout")
        self.back_btn.clicked.connect(lambda: self.parent.return_to_login())
        main_layout.addWidget(self.back_btn)

        # ---- Load data ----
        self.load_voters()
        self.load_candidates()
        self.load_votes()
        self.load_history()

    # ====================================
    # Data Handlers
    # ====================================

    def load_voters(self):
        rows = get_unverified_voters()
        self.voters_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            sid = row["voter_id"] if "voter_id" in row.keys() else f"S{str(row['id']).zfill(4)}"
            full_name = f"{row['fname']} {row['lname']}"
            data = [row["id"], sid, full_name, row["password"]]
            for c, val in enumerate(data):
                self.voters_table.setItem(r, c, QTableWidgetItem(str(val)))

    def verify_voter(self):
        row = self.voters_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a voter to verify.")
            return

        voter_id = int(self.voters_table.item(row, 0).text())
        name = self.voters_table.item(row, 2).text()
        verify_voter(voter_id)
        log_history("Verify Voter", f"Verified voter: {name}")
        QMessageBox.information(self, "Verified", f"{name} has been verified.")
        self.load_voters()
        self.load_history()

    def load_candidates(self):
        rows = get_candidates()
        self.candidates_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            data = [row["id"], row["position"], row["name"]]
            for c, val in enumerate(data):
                self.candidates_table.setItem(r, c, QTableWidgetItem(str(val)))
        self.load_votes()  # also refresh votes table

    def add_candidate(self):
        position, ok = QInputDialog.getText(self, "Add Candidate", "Position:")
        if not ok or not position.strip():
            return
        name, ok = QInputDialog.getText(self, "Add Candidate", "Candidate Name:")
        if not ok or not name.strip():
            return
        create_candidate(position, name)
        QMessageBox.information(self, "Added", f"Candidate '{name}' added.")
        self.load_candidates()
        self.load_history()

    def edit_candidate(self):
        row = self.candidates_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a candidate to edit.")
            return

        cand_id = int(self.candidates_table.item(row, 0).text())
        old_position = self.candidates_table.item(row, 1).text()
        old_name = self.candidates_table.item(row, 2).text()

        position, ok = QInputDialog.getText(self, "Edit Candidate", "New Position:", text=old_position)
        if not ok or not position.strip():
            return
        name, ok = QInputDialog.getText(self, "Edit Candidate", "New Name:", text=old_name)
        if not ok or not name.strip():
            return
        edit_candidate(cand_id, position, name)
        QMessageBox.information(self, "Updated", "Candidate updated successfully.")
        self.load_candidates()
        self.load_history()

    def delete_candidate(self):
        row = self.candidates_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a candidate to delete.")
            return

        cand_id = int(self.candidates_table.item(row, 0).text())
        name = self.candidates_table.item(row, 2).text()

        confirm = QMessageBox.question(self, "Delete", f"Delete candidate '{name}'?")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        remove_candidate(cand_id)
        QMessageBox.information(self, "Deleted", f"Candidate '{name}' removed.")
        self.load_candidates()
        self.load_history()

    def load_votes(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT position, name, votes FROM candidates ORDER BY position, votes DESC")
        rows = c.fetchall()
        conn.close()

        self.votes_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            data = [row["position"], row["name"], row["votes"]]
            for c, val in enumerate(data):
                self.votes_table.setItem(r, c, QTableWidgetItem(str(val)))

    def load_history(self):
        rows = get_history_records(limit=30)
        self.history_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            data = [row["action"], row["details"], row["timestamp"]]
            for c, val in enumerate(data):
                self.history_table.setItem(r, c, QTableWidgetItem(str(val)))
