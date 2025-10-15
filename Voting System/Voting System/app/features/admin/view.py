
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QLineEdit, QFormLayout, QMessageBox)
from features.items import service as svc

class AdminWidget(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent = parent_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel('<b>Admin Panel</b>'))

        # Voter verification area
        self.layout.addWidget(QLabel('Unverified Voters:'))
        self.unverified_list = QListWidget()
        self.layout.addWidget(self.unverified_list)
        h = QHBoxLayout()
        self.verify_btn = QPushButton('Verify Selected')
        self.refresh_btn = QPushButton('Refresh')
        h.addWidget(self.verify_btn); h.addWidget(self.refresh_btn)
        self.layout.addLayout(h)
        self.verify_btn.clicked.connect(self.handle_verify)
        self.refresh_btn.clicked.connect(self.refresh_unverified)

        # Add position and candidate
        self.layout.addWidget(QLabel('Add Position'))
        form = QFormLayout()
        self.pos_title = QLineEdit(); form.addRow('Title:', self.pos_title)
        self.add_pos_btn = QPushButton('Add Position'); form.addRow(self.add_pos_btn)
        self.layout.addLayout(form)
        self.add_pos_btn.clicked.connect(self.handle_add_position)

        self.layout.addWidget(QLabel('Add Candidate'))
        form2 = QFormLayout()
        self.cand_name = QLineEdit()
        self.cand_pos_id = QLineEdit()  # admin will specify position id (simple)
        form2.addRow('Name:', self.cand_name); form2.addRow('Position ID:', self.cand_pos_id)
        self.add_cand_btn = QPushButton('Add Candidate'); form2.addRow(self.add_cand_btn)
        self.layout.addLayout(form2)
        self.add_cand_btn.clicked.connect(self.handle_add_candidate)

        # Results area
        self.layout.addWidget(QLabel('Results:'))
        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)
        self.refresh_results_btn = QPushButton('Refresh Results')
        self.layout.addWidget(self.refresh_results_btn)
        self.refresh_results_btn.clicked.connect(self.refresh_results)

        self.refresh_unverified()
        self.refresh_results()

    def refresh_unverified(self):
        self.unverified_list.clear()
        rows = svc.list_unverified_voters()
        for r in rows:
            self.unverified_list.addItem(f"{r['id']} — {r['student_id']} — {r['name']}")

    def handle_verify(self):
        it = self.unverified_list.currentItem()
        if not it:
            QMessageBox.warning(self, 'No selection', 'Select a voter to verify.')
            return
        vid = int(it.text().split(' — ')[0])
        svc.approve_voter(vid)
        QMessageBox.information(self, 'Verified', 'Voter approved.')
        self.refresh_unverified()

    def handle_add_position(self):
        t = self.pos_title.text().strip()
        if not t:
            QMessageBox.warning(self, 'Missing', 'Position title required.')
            return
        ok = svc.add_position(t)
        if ok:
            QMessageBox.information(self, 'Added', 'Position added.')
            self.pos_title.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Could not add position (maybe exists).')

    def handle_add_candidate(self):
        n = self.cand_name.text().strip()
        pid = self.cand_pos_id.text().strip()
        if not n or not pid:
            QMessageBox.warning(self, 'Missing', 'Provide name and position id.')
            return
        try:
            pidn = int(pid)
        except:
            QMessageBox.warning(self, 'Invalid', 'Position id must be a number.')
            return
        svc.add_candidate(n, pidn)
        QMessageBox.information(self, 'Added', 'Candidate added.')
        self.cand_name.clear(); self.cand_pos_id.clear()

    def refresh_results(self):
        self.results_list.clear()
        rows = svc.get_results()
        for r in rows:
            self.results_list.addItem(f"{r['position']} — {r['candidate']} — {r['votes']}")
