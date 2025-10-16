from dataclasses import dataclass

@dataclass
class Candidate:
    id: int = None
    position: str = ''
    name: str = ''
    votes: int = 0


@dataclass
class Voter:
    id: int = None
    voter_id: str = ''  # Unique ID starting with 'S'
    fname: str = ''
    mname: str = ''
    lname: str = ''
    password: str = ''
    verified: int = 0


@dataclass
class History:
    id: int = None
    action: str = ''
    details: str = ''
    timestamp: str = ''
