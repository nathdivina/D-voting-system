from app.core.db import get_connection, hash_password, generate_voter_id

def find_verified_voter(identifier, password):
    """
    Find a verified voter using either their last name or voter_id + password.
    """
    conn = get_connection()
    c = conn.cursor()
    hashed = hash_password(password)

    c.execute("""
        SELECT * FROM voters
        WHERE verified = 1 AND password = ?
        AND (lname = ? OR voter_id = ?)
    """, (hashed, identifier, identifier))

    row = c.fetchone()
    conn.close()
    return row


def insert_voter(fname, mname, lname, password):
    """
    Register a new voter and generate a unique voter_id.
    Returns the generated voter_id for display.
    """
    conn = get_connection()
    c = conn.cursor()

    voter_id = generate_voter_id()
    hashed = hash_password(password)

    c.execute("""
        INSERT INTO voters (voter_id, fname, mname, lname, password, verified)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (voter_id, fname.strip(), mname.strip(), lname.strip(), hashed))

    conn.commit()
    conn.close()
    return voter_id  # Return voter ID so it can be shown after registration


def get_unverified_voters():
    """
    Return all unverified voters.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM voters WHERE verified = 0")
    rows = c.fetchall()
    conn.close()
    return rows


def verify_voter(voter_id):
    """
    Mark a voter as verified using their numeric 'id' (admin side).
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE voters SET verified = 1 WHERE id = ?", (voter_id,))
    conn.commit()
    conn.close()
