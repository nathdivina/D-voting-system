import re
from app.features.login.repository import find_verified_voter, insert_voter

def validate_password(password: str) -> str:
    if len(password) < 12:
        return "Password must be at least 12 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must include an uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must include a lowercase letter."
    if not re.search(r"\d", password):
        return "Password must include a number."
    if not re.search(r"[^A-Za-z0-9]", password):
        return "Password must include a special character."
    return ""

def register_voter(fname, mname, lname, password):
    fname = fname.strip().capitalize()
    mname = mname.strip().capitalize() if mname else ''
    lname = lname.strip().capitalize()

    err = validate_password(password)
    if err:
        return None, err

    voter_id = insert_voter(fname, mname, lname, password)
    return voter_id, None

def login_voter(identifier, password):
    return find_verified_voter(identifier.strip().capitalize(), password)
