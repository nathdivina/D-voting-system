
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout,
                             QComboBox, QMessageBox, QScrollArea, QWidgetItem)
from features.items import service as svc

class VoterWidget(QWidget):
    def __init__(self, voter=None):
        super().__init__()
        self.voter = voter
        self.layout = QVBoxLayout(); self.setLayout(self.layout)
        self.layout.addWidget(QLabel(f'<b>Welcome, {voter["name"]}</b>'))

        self.layout.addWidget(QLabel('Select one candidate per position:'))
        self.position_selectors = {}  # position_id -> QComboBox

        positions = svc.list_positions()
        for p in positions:
            pid = p['id']; title = p['title']
            self.layout.addWidget(QLabel(f'Position: {title} (id: {pid})'))
            combo = QComboBox()
            combo.addItem('--- Select ---', 0)
            cands = svc.list_candidates_by_position(pid)
            for c in cands:
                combo.addItem(c['name'], c['id'])
            self.position_selectors[pid] = combo
            self.layout.addWidget(combo)

        self.submit_btn = QPushButton('Submit Votes')
        self.layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.handle_submit)

    def handle_submit(self):
        selections = {}
        for pid, combo in self.position_selectors.items():
            cid = combo.currentData()
            if cid and cid != 0:
                selections[pid] = cid
        if not selections:
            QMessageBox.warning(self, 'No selection', 'Choose at least one candidate to vote for.')
            return
        ok, msg = svc.cast_votes_for_voter(self.voter['id'], selections)
        if ok:
            QMessageBox.information(self, 'Voted', msg)
        else:
            QMessageBox.warning(self, 'Error', msg)
