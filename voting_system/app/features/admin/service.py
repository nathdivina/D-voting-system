from app.features.admin.repository import (
    list_unverified_voters,
    verify_voter_db,
    list_candidates,
    add_candidate,
    update_candidate,
    delete_candidate,
    get_history
)

# 🧩 VOTER MANAGEMENT

def get_unverified_voters():
    """Fetch all voters who have not yet been verified."""
    return list_unverified_voters()

def verify_voter(voter_id):
    """Mark a voter as verified."""
    verify_voter_db(voter_id)


# 🧩 CANDIDATE MANAGEMENT

def get_candidates():
    """Return all candidates ordered by votes."""
    return list_candidates()

def create_candidate(position, name):
    """Add a new candidate to the system."""
    add_candidate(position.strip(), name.strip())

def edit_candidate(cid, position, name):
    """Update existing candidate information."""
    update_candidate(cid, position.strip(), name.strip())

def remove_candidate(cid):
    """Remove a candidate from the system."""
    delete_candidate(cid)


# 🧩 HISTORY LOGGING

def get_history_records(limit=200):
    """Retrieve recent system actions for the admin view."""
    return get_history(limit)
