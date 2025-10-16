from app.features.voter.repository import list_positions_with_candidates, increment_vote

def get_ballot():
    return list_positions_with_candidates()

def cast_votes(selections: dict):
    # selections: {position: candidate_id, ...}
    for pos, cid in selections.items():
        increment_vote(cid)
