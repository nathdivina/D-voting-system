from dataclasses import dataclass

@dataclass
class Voter:
    id: int = None
    fname: str = ''
    mname: str = ''
    lname: str = ''
    password: str = ''
    verified: bool = False
