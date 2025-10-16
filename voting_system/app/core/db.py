import sqlite3
from datetime import datetime
import hashlib
import os

DB_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'voting_system.db')

def get_connection():
    """Connect to SQLite database and return connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database tables if they do not exist."""
    conn = get_connection()
    c = conn.cursor()

    # Voters table (includes voter_id)
    c.execute('''CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id TEXT UNIQUE,
        fname TEXT NOT NULL,
        mname TEXT,
        lname TEXT NOT NULL,
        password TEXT NOT NULL,
        verified INTEGER DEFAULT 0
    )''')

    # Candidates table
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position TEXT NOT NULL,
        name TEXT NOT NULL,
        votes INTEGER DEFAULT 0
    )''')

    # History table
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        details TEXT,
        timestamp TEXT NOT NULL
    )''')

    conn.commit()
    conn.close()

def log_history(action, details):
    """Log admin actions such as add, edit, delete, verify."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (action, details, timestamp) VALUES (?, ?, ?)",
        (action, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_voter_id() -> str:
    """
    Generate unique voter ID like S001, S002, etc.
    Ensures IDs are unique even after deletions.
    """
    conn = get_connection()
    c = conn.cursor()

    # Get the highest numeric part of voter_id
    c.execute("SELECT voter_id FROM voters WHERE voter_id LIKE 'S%' ORDER BY voter_id DESC LIMIT 1")
    last_id = c.fetchone()
    conn.close()

    if last_id:
        try:
            # Extract numeric part and increment
            last_num = int(last_id["voter_id"][1:])
            new_id = f"S{last_num + 1:03d}"
        except ValueError:
            new_id = "S001"
    else:
        new_id = "S001"

    return new_id
