
import hashlib
from . import repository as repo

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

# Voter flows
def register_voter(student_id, name, password):
    ph = hash_password(password)
    return repo.create_voter(student_id, name, ph)

def authenticate_voter(student_id, password):
    r = repo.find_voter_by_student(student_id)
    if not r:
        return None, 'No such student id'
    ph = hash_password(password)
    if r['password_hash'] != ph:
        return None, 'Invalid password'
    if r['verified'] == 0:
        return None, 'Account not verified by admin'
    return r, 'OK'

def list_unverified_voters():
    return repo.list_unverified_voters()

def approve_voter(voter_id):
    return repo.verify_voter(voter_id)

# Admin simple auth (fixed credentials)
def authenticate_admin(username, password):
    return username == 'admin' and password == '1234'

# Positions & candidates
def add_position(title):
    return repo.add_position(title)

def list_positions():
    return repo.list_positions()

def add_candidate(name, position_id):
    return repo.add_candidate(name, position_id)

def list_candidates_by_position(position_id):
    return repo.list_candidates_by_position(position_id)

# Voting
def cast_votes_for_voter(voter_id, selections: dict):
    # selections: {position_id: candidate_id, ...}
    # Validate that voter hasn't already voted for any of the positions
    for pos_id, cand_id in selections.items():
        if repo.has_voted_for_position(voter_id, pos_id):
            return False, f'You already voted for position id {pos_id}'
    # Cast all votes
    for pos_id, cand_id in selections.items():
        ok, msg = repo.cast_vote(voter_id, cand_id, pos_id)
        if not ok:
            return False, msg
    return True, 'All votes recorded'

def get_results():
    return repo.get_results()
