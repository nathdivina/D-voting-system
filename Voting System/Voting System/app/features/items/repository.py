
from core.db import get_connection

# Voter operations
def create_voter(student_id, name, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO voters (student_id, name, password_hash) VALUES (?, ?, ?)', (student_id, name, password_hash))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def find_voter_by_student(student_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT * FROM voters WHERE student_id = ?', (student_id,))
    r = cur.fetchone(); conn.close()
    return r

def list_unverified_voters():
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT * FROM voters WHERE verified = 0')
    rows = cur.fetchall(); conn.close(); return rows

def verify_voter(voter_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('UPDATE voters SET verified = 1 WHERE id = ?', (voter_id,))
    conn.commit(); conn.close()

# Positions & Candidates
def add_position(title):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute('INSERT INTO positions (title) VALUES (?)', (title,))
        conn.commit(); return True
    except Exception:
        return False
    finally:
        conn.close()

def list_positions():
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT * FROM positions ORDER BY id'); rows = cur.fetchall(); conn.close(); return rows

def add_candidate(name, position_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('INSERT INTO candidates (name, position_id) VALUES (?, ?)', (name, position_id))
    conn.commit(); conn.close()

def list_candidates_by_position(position_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT * FROM candidates WHERE position_id = ?', (position_id,))
    rows = cur.fetchall(); conn.close(); return rows

# Votes
def has_voted_for_position(voter_id, position_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as cnt FROM votes WHERE voter_id = ? AND position_id = ?', (voter_id, position_id))
    r = cur.fetchone(); conn.close(); return r['cnt'] > 0

def cast_vote(voter_id, candidate_id, position_id):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute('INSERT INTO votes (voter_id, candidate_id, position_id) VALUES (?, ?, ?)', (voter_id, candidate_id, position_id))
        conn.commit(); return True, 'Vote recorded'
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_results():
    conn = get_connection(); cur = conn.cursor()
    cur.execute('''
        SELECT p.title as position, c.name as candidate, COUNT(v.id) as votes
        FROM candidates c
        LEFT JOIN votes v ON c.id = v.candidate_id
        JOIN positions p ON c.position_id = p.id
        GROUP BY c.id, p.title ORDER BY p.id, votes DESC
    ''')
    rows = cur.fetchall(); conn.close(); return rows
