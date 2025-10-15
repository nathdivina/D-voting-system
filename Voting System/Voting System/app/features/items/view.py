from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from .service import list_candidates, cast_vote

class VotePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Vote for your Candidate"))

        for cand in list_candidates():
            btn = QPushButton(f"{cand[1]} - {cand[2]}")
            btn.clicked.connect(lambda _, cid=cand[0]: cast_vote(cid))
            layout.addWidget(btn)

        self.setLayout(layout)
