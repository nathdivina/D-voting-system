from app.core.db import get_connection, log_history

def list_positions_with_candidates():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT position FROM candidates GROUP BY position')
    rows = [r['position'] for r in c.fetchall()]
    conn.close()
    result = {}
    # fetch candidates per position
    conn = get_connection()
    c = conn.cursor()
    for pos in rows:
        c.execute('SELECT * FROM candidates WHERE position=? ORDER BY votes DESC, id ASC', (pos,))
        result[pos] = c.fetchall()
    conn.close()
    return result

def increment_vote(candidate_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE candidates SET votes = votes + 1 WHERE id=?', (candidate_id,))
    conn.commit()
    conn.close()
    log_history('vote', f'candidate_id={candidate_id}')

