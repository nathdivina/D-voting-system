from dataclasses import dataclass

@dataclass
class CandidateChoice:
    id: int = None
    position: str = ''
    name: str = ''
    votes: int = 0
