from app.core.db import get_connection, log_history

# 🧩 VOTER MANAGEMENT

def list_unverified_voters():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, fname, mname, lname, password FROM voters WHERE verified=0')
    rows = c.fetchall()
    conn.close()
    return rows

def verify_voter_db(voter_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE voters SET verified=1 WHERE id=?', (voter_id,))
    conn.commit()
    conn.close()
    log_history('verify_voter', f'verified voter id={voter_id}')


# 🧩 CANDIDATE MANAGEMENT

def list_candidates():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM candidates ORDER BY votes DESC, id ASC')
    rows = c.fetchall()
    conn.close()
    return rows

def add_candidate(position, name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO candidates (position, name, votes) VALUES (?, ?, 0)', (position, name))
    conn.commit()
    cid = c.lastrowid
    conn.close()
    log_history('add_candidate', f'id={cid}, position={position}, name={name}')

def update_candidate(cid, position, name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE candidates SET position=?, name=? WHERE id=?', (position, name, cid))
    conn.commit()
    conn.close()
    log_history('update_candidate', f'id={cid}, position={position}, name={name}')

def delete_candidate(cid):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM candidates WHERE id=?', (cid,))
    conn.commit()
    conn.close()
    log_history('delete_candidate', f'id={cid}')


# 🧩 HISTORY LOGGING

def get_history(limit=200):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM history ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
