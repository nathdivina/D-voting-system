
from dataclasses import dataclass

@dataclass
class Voter:
    id: int
    student_id: str
    name: str
    verified: int

@dataclass
class Position:
    id: int
    title: str

@dataclass
class Candidate:
    id: int
    name: str
    position_id: int
